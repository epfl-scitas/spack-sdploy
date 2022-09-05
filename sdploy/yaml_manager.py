# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                       #
# SCITAS STACK DEPLOYMENT 2022, EPFL                                    #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import spack
import spack.util
import spack.util.spack_yaml as spyaml
import collections.abc
from pdb import set_trace as st

class ReadYaml(object):
    """YAML file manager

    Provide methods to read and write YAML files to and from dictionaries.
    Provide methods to update dictionaries under certain conditions.

    The choice between ruamel.yaml and pyyaml is not clear. For the moment
    it follows spack choice, but this version dates from August 2016 (0.11.15).
    The latest release is version 0.17.21 (February 2022).

    ruamel.yaml support YAML 1.2 / PyYAML support YAML 1.1
    YAML 1.2 was released in 2009.
    There are rumours that maintenance for PyYAML was not always assured."""

    def __init__(self):
        """Set configuration directory"""

        self.root = None
        self.data = None
        self.cursor = []

        ### NEW FORMAT
        self.data = None
        self.config = None
        self.platform = None
        self.tokens = None

    def read(self, filename, **kwargs):
        """Read yaml file into data object"""

        with open(filename) as f:
            self.data = spyaml.load_config(f, **kwargs)
        return self.data

    def get_data(self, filename):
        """Returns the data read"""

        with open(filename) as f:
            return(spyaml.load_config(f))

    def list(self):
        """Display configuration"""

        print(spyaml.round_trip_dump(self.data))

    #
    #
    # THESE ARE THE NEW FUNCTIONS USED POTENTIALLY IN EVERY CLASS
    #
    #

    def replace_tokens(self, data):
        """Reads tokens from platform file and executes replacement.
        `data` is a dictionary where the replacements will happen.
        Replacements are done in place."""

        self.tokens = self._read_tokens(self.platform_file)
        for key, value in self.tokens.items():
            self._do_replace_tokens(data, '<' + str(key) + '>', str(value))

    def _read_tokens(self, platform_file):
        """Return dict of keys to be replaced in stack file

        Replacements are found under the common:variables key:

            platform:
              variables:
                key1: option1
                key2: option2
                ...

        This method will return a dict like this:

            {key1: option1, key2, option2, ...}
        """

        if not platform_file:
            platform_file = self.platform_file

        if not os.path.exists(platform_file):
            common.data['platform']['tokens'] = {}
        else:
            common = ReadYaml()
            common.read(platform_file)
            
        return(common.data['platform']['tokens'])

    def _do_replace_tokens(self, d, pat, rep):
        """Attempt to replace stuff in YAML file

        >>> IN PLACE REPLACEMENT <<<

        d - yaml file in form of python dicy.
        pat - pattern to look for, par exemple: '<<id>>'.
        rep - replacement string, par exemple: 'xy: z')."""

        if isinstance(d, dict):
            for k in d:
                if isinstance(d[k], str):
                    d[k] = d[k].replace(pat, rep)
                else:
                   self._do_replace_tokens(d[k], pat, rep)
        if isinstance(d, list):
            for idx, elem in enumerate(d):
                if isinstance(elem, str):
                    d[idx] = elem.replace(pat, rep)
                else:
                   self._do_replace_tokens(d[idx], pat, rep)

    def read_filters(self, platform_file):
        """Return dict of keys to be replaced in stack file

        Replacements are found under the platform:filters key:

            platform:
              filters:
                key1: option1
                key2: option2
                ...

        This method will return a dict like this:

            {key1: option1, key2, option2, ...}
        """

        if not platform_file:
            platform_file = self.platform_file

        if not os.path.exists(platform_file):
            common.data['platform']['filters'] = {}
        else:
            common = ReadYaml()
            common.read(platform_file)
        return(common.data['platform']['filters'])

    def group_sections(self, dic, section):
        """Returns dictionary composed of common sections

        In the stack.yaml file there can be to different key that both are
        related to packages or to PE. This function will group all section
        which has section value in section key"""

        tmp = {}
        for key in dic:
            if dic[key]['metadata']['section'] == section:
                dic[key].pop('metadata')
                tmp[key] = dic[key]
        return(tmp)

    #
    #
    # END
    #
    #






    def do_choose(self, stack, dic, token):
        """Replace token keys in dictionary

        Example:

        Suppose the following key is found in stack:

            gpu: { nvidia: cuda, amd: rocm }

        then, if token = {gpu: nvidia} the 'key' in the stack will no longer be
        a dictionary and it will be {'gpu': 'cuda'}.

        CAVEATS: although this function works, it needs major revision. This
        function does not work if more complicated nested dictionaries are used."""

        for k, v in dic.items():
            if (isinstance(v, dict)
                and k in token.keys()):
                self._update(stack, self._dic_from_list({}, self._cursor + [k] +
                                                        [v[token[k]]], True))
            elif isinstance(v, dict):
                self._cursor.append(k)
                self.do_choose(stack, v, token)
                self._cursor.pop(-1)

            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        self._cursor.append(k)
                        self.do_choose(stack, item, token)
                        self._cursor.pop(-1)


    def read_choices(self, platform_file):
        """Return dict of keys to be replaced in stack file

        Replacements are found under the common:filter key:

            common:
              filters:
                key1: option1
                key2: option2
                ...

        This method will return a dict like this:

            {key1: option1, key2, option2, ...}
        """

        common = ReadYaml()
        common.read(platform_file)
        return(common.data['common']['filters'])

    def read_replacements(self, platform_file):
        """Return dict of keys to be replaced in stack file

        Replacements are found under the common:variables key:

            common:
              variables:
                key1: option1
                key2: option2
                ...

        This method will return a dict like this:

            {key1: option1, key2, option2, ...}
        """

        if not os.path.exists(platform_file):
            common.data['platform']['variables'] = {}
        else:
            common = ReadYaml()
            common.read(platform_file)

        return(common.data['common']['variables'])

    def do_replace(self, d, pat, rep):
        """Attempt to replace stuff in YAML file

        d - yaml file in form of python dicy.
        pat - pattern to look for, par exemple: '<<id>>'.
        rep - replacement string, par exemple: 'xy: z')."""

        if isinstance(d, dict):
            for k in d:
                if isinstance(d[k], str):
                    d[k] = d[k].replace(pat, rep)
                else:
                   self.do_replace(d[k], pat, rep)
        if isinstance(d, list):
            for idx, elem in enumerate(d):
                if isinstance(elem, str):
                    d[idx] = elem.replace(pat, rep)
                else:
                   self.do_replace(d[idx], pat, rep)

    def _update(self, d, u):
        """Update nested dictionary (d) with given dictionary (u)"""

        # update(stack, {'intel': {'stable': {'gpu': 'edu'}}})
        # self.stack.get('core_pkgs').get('packages')
        tmp = {'core_pkgs': {'packages': {'cmake@3.9.18': {'gpu': '+cuda cuda_arch=cuda_arch'}}}}
        if u == tmp:
            pass
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                if isinstance(d.get(k, {}), collections.abc.Mapping):
                    d[k] = self._update(d.get(k, {}), v)
                if isinstance(d.get(k, {}), list):
                    d[k] = self._update(d.get(k, {})[0], v)
            else:
                d[k] = v
        return d


    def _dic_from_list(self, d, keylist, lastvalue=False):
        """Return nested dictionary whose keys are given by cursor

        Examples:

          dic_from_list({}, ['a', 'b', 'c'], lastvalue=False)
              -> {'a': {'b': {'c'}}}

          dic_from_list({}, ['a', 'b', 'c'], lastvalue=True)
              -> {'a': {'b': 'c'}}"""

        if lastvalue:
            v = keylist.pop(-1)
            lastvalue=False
            return(self._dic_from_list({ keylist.pop(-1) : v }, keylist))
        while keylist:
            return(self._dic_from_list({ keylist.pop(-1) : d }, keylist))
        return(d)
