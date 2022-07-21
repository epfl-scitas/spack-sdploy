from pdb import set_trace as st

from collections.abc import MutableMapping
from copy import deepcopy
from .yaml_manager import ReadYaml


class Packages(ReadYaml):
    """Manage the packages section in stack.yaml"""

    def __init__(self, platform_file, stack_file):
        """Declare class structs"""

        # yaml files
        self.stack_file = stack_file
        self.platform_file = platform_file
        # data
        self.data = {}
        self.stack = {}
        # self.specs = [] not used ???
        # for jinja parsing
        self.pkg_defs = {}
        self.pe = {}
        # used to write packages.yaml
        self.pkgs_yaml = {}
        # options & replacements
        self.options = {}
        self.replacements = {}

    def __call__(self, section):
        """Populate class structs"""

        # Reads stack.yaml into self.data
        self.read(self.stack_file)

        # Groups entries whose section = <section> in self.stack
        self.stack = self.group_sections(deepcopy(self.data), section)

        # Execute replacements (common:variables)
        self.replace_tokens = self.read_replacements(self.platform_file)
        for key, value in self.replace_tokens.items():
            self.do_replace(self.stack, '<' + str(key) + '>', str(value))

        # Read selections
        self.options = self.read_options()

        # Set up dictionaries for later parsing
        for list_name, list_pkgs in self.stack.items():
            self.pkg_defs[list_name] = []
            for pkg in list_pkgs['packages']:
                if isinstance(pkg, str):
                    self.pkg_defs[list_name].append(pkg)
                if isinstance(pkg, dict):
                    spec = self.spec_from_def(pkg)
                    self.pkg_defs[list_name].append(spec)

        self.create_pe_dict()
        self.create_packages_yaml()

    def create_pe_dict(self):
        """Create dictionary for parsing jinja template with the package list
        name, the compilers it should use and any dependencies."""

        for pkg_list in self.stack.keys():
            self.pe[pkg_list] = { 'pe': self.stack[pkg_list]['pe'] }
            if 'dependencies' in self.stack[pkg_list]:
                self.pe[pkg_list]['dependencies'] = self.stack[pkg_list]['dependencies']

    def create_packages_yaml(self):
        """Read self.stack dict and create self.pkgs_yaml

        The self.pkgs_yaml dictionary will contain the data ready to
        be used in the jinja template.

        Minimum requirements for adding a package to packages.yaml:
        - the package contains the default key;
        - the package contains at least on of: (version or variants) or externals.

        The default section is only an indicator. All the information will be
        copied to packages.yaml. Only the options will be applied and eventually
        a dependencies section.

        This method will create a NEW DICTIONARY based on self.stack['default']
        """

        for list_name, list_pkgs in self.stack.items():
            for pkg in list_pkgs['packages']:
                if isinstance(pkg, dict):
                    pkg_name = list(pkg.keys())[0]
                    if 'default' in pkg[pkg_name]:
                        default_specs = pkg[pkg_name]['default']
                        specs = []
                        # All of this below will go into a separate method
                        # Check for option keys and select in accordance
                        selected_specs = self.spec_select(self.options, default_specs)
                        specs.append(selected_specs)
                        # Check for dependencies
                        # This will go into a separate method
                        if 'dependencies' in default_specs:
                            for d in default_specs.get('dependencies'):
                                specs.append('^' + d.strip())
                        # Add to variants if exists
                        if 'variants' in default_specs:
                            variants = specs.append(default_specs['variants'])
                        else:
                            variants = specs
                        # At this moment, 'variants' could be an empty list
                        # Finnaly add specs to dict
                        #if not (list_name in self.pkgs_yaml):
                        #    self.pkgs_yaml[list_name] = {pkg_name: {}}
                        self.pkgs_yaml[pkg_name] = default_specs
                        # Remove metadata
                        # This will go into a seperate method
                        if 'gpu' in self.pkgs_yaml[pkg_name]:
                            self.pkgs_yaml[pkg_name].pop('gpu')
                        if 'dependencies' in self.pkgs_yaml[pkg_name]:
                            self.pkgs_yaml[pkg_name].pop('dependencies')
                        if 'mpi' in self.pkgs_yaml[pkg_name]:
                            self.pkgs_yaml[pkg_name].pop('mpi')


    def spec_from_def(self, pkg_def):
        """Return spec from definition schema found in stack.yaml

        The spec goes to spack.yaml: this method creates a string for
        the package spec and add this spec (string) to self.defs dict.
        This is the dict that later will be used to parse the template."""

        pkg_name = list(pkg_def.keys())[0]
        spec = [pkg_name]
        settings = pkg_def.get(pkg_name)
        # Process variants
        if 'variants' in settings:
            spec.append(settings.get('variants'))
        # Process spec options
        selected_specs = self.spec_select(self.options, settings)
        if selected_specs:
            spec.append(selected_specs)
        # Process dependencies
        if 'dependencies' in settings:
            for d in settings.get('dependencies'):
                spec.append('^' + d.strip())

        return(' '.join(spec).strip())

    def read_options(self, platform_file = None):
        """Return dict of keys to be replaced in stack file"""

        if not platform_file:
            platform_file = self.platform_file
        common = ReadYaml()
        common.read(platform_file)
        return(common.data['common']['filters'])

    def spec_select(self, options, settings):
        """Return string of selected specs"""

        selection = []
        for opt in options.keys():
            if opt in settings:
                if settings.get(opt).get(options.get(opt)) is None:
                    print(f'Found {opt}:{options.get(opt)} selector but no matching'
                    f' {options.get(opt)} option in stack.yaml')
                    print(f'Exiting...')
                    exit(1)
                selection.append(settings.get(opt).get(options.get(opt)))
        return(' '.join(selection))

    def add_to_packages_yaml(self, pkg_name, selected, options, default_pkg):
        """Add previous selected options (in any) to the default section.
        This prevents the user from having to choose the specs twice."""

        selected_specs = self.spec_select(options, default_pkg)

        # VERY BUGGY INSTRUCTION !!!
        default_pkg['variants'] = ' '.join([default_pkg['variants'], selected, selected_specs])

        for opt in options.keys():
            if opt in default_pkg:
                default_pkg.pop(opt)

        return({pkg_name: default_pkg})

    def create_definitions(self):
        """Create definitions dict for template"""

        for k,v in self.stack.items():
            pkg_list = []
            for pkg in v['packages']:
                pkg_list.append(pkg)
            st()
            self.defs[k] = v['packages'][0]

    def flatten_dict(self, d: MutableMapping, parent_key: str = '', sep: str = '_'):
        """Returns a flat dict

        Return a 1-depth dict (flat) whose elements are formed by composing
        the nested dicts nodes using the separator sep.
        {'a':1, 'b':{'c':2}} -> {'a':1, 'b_c':2}
        origin: freecodecamp.org"""

        return dict(self._flatten_dict_gen(d, parent_key, sep))

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

    def _flatten_dict_gen(self, d, parent_key, sep):
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                yield from self.flatten_dict(v, new_key, sep=sep).items()
            else:
                yield new_key, v
