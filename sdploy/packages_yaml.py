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

import llnl.util.tty as tty
import spack.schema

from copy import deepcopy
import inspect

from .stack_file import StackFile, FilterException
from .yaml_manager import ReadYaml
from .util import *

class PackagesYaml(StackFile):
    """Manage the packages section in stack.yaml"""

    def __init__(self, config):
        """Declare class structs"""

        super().__init__(config)

        # These variables will be used in StackFile class.
        # Each command that write an Yaml file must define these 4 variables.
        # This technique allows for individual command customization of each
        # one of these parameters and at the same time the reuse of the functions
        # all gathered in a single module.
        self.templates_path = self.config.templates_path
        self.template_file = self.config.packages_yaml_template
        self.yaml_path = self.config.spack_config_path
        self.yaml_file = self.config.packages_yaml

        # Used to create packages.yaml:
        self.defaults = {}
        self.externals = {}
        self.providers = {}
        self.all_prefs = {}

        # Groups entries whose section = <section> in self.stack
        self.stack = {} # The data grouped by `section = packages`
        self.stack = self.group_sections(deepcopy(self.data), 'packages')


    def packages_yaml_packages(self):
        """Creates a sub-dictionary containing the packages and their specs that
        will be given to jinja2 template.

            pkgs_yaml_pkgs - this dict
        """

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        for pkg_list_name, pkg_list_cfg in self.stack.items():
            tty.debug(f'Entering package list: {pkg_list_name}')

            for pkg_list in pkg_list_cfg.get('packages'):
                if not isinstance(pkg_list, dict):
                    continue

                if len(pkg_list.keys()) > 1:
                    raise KeyError()

                pkg_name = list(pkg_list.keys())[0]
                pkg_attributes = pkg_list[pkg_name]

                tty.debug(f'Reading package: {pkg_name}')

                if not 'default' in pkg_attributes:
                    continue

                defaults = pkg_attributes['default']

                self.defaults[pkg_name] = {}
                for attr in ['version', 'variants', 'buildable']:
                    result = None
                    if attr not in defaults:
                        continue

                    tty.debug(f'Reading "{attr}": {defaults[attr]}')
                    try:
                        _packages_yaml_pkg = getattr(PackagesYaml, '_packages_yaml_packages_' + attr, )
                        result =  _packages_yaml_pkg(self, defaults[attr])
                    except FilterException as fe:
                        tty.debug(f'Ignoring package {pkg_name} in `packages.yaml` due to missing value for {fe.filter_value} in filter {fe.filter}')

                    if result:
                        self.defaults[pkg_name][attr] = result

    def _packages_yaml_packages_version(self, version_attributes):
        """Adds version to dictionary"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        version = self._handle_filter(version_attributes)
        return version


    def _packages_yaml_packages_variants(self, variants_attributes):
        """Adds variants to dictionary"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        variants = []
        if 'common' in variants_attributes:
            variants.append(variants_attributes.get('common'))

        variants.extend(self._handle_filter(variants_attributes))
        return self._remove_newline(' '.join(variants))

    def _packages_yaml_packages_buildable(self, buildable):
        """Adds version to dictionary"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        return buildable

    def packages_yaml_external(self):
        """Creates a sub-dictionary containing the packages and their specs that
        will be given to jinja2 template.

            pkgs_external - this dict
        """

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        for pkg_list_cfg in self.stack.values():
            for pkg_list in pkg_list_cfg['packages']:
                if isinstance(pkg_list, dict):
                    for pkg_name, pkg_attributes in pkg_list.items():
                        if not 'externals' in pkg_attributes:
                            continue

                        self.externals[pkg_name] = [dict(x) for x in pkg_attributes['externals']]
                        # externals = pkg_attributes.get('external')

    def packages_yaml_providers(self):
        """Creates a sub-dictionary containing the providers section that will
        be given to jinja2 template.

            pkgs_providers - this dict
        """

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        platform = ReadYaml()
        platform.read(self.config.platform_yaml)
        if 'providers' in platform.data['platform']:
            self.providers = platform.data['platform']['providers']

    def packages_yaml_all_preferences(self):
        """Creates a sub-dictionary containing the common preferences section
        to be given to jinja2 template.

            pkgs_all_prefs - this dict
        """

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        platform = ReadYaml()
        platform.read(self.config.platform_yaml)
        if 'preferences' in platform.data['platform']:
            self.all_prefs = platform.data['platform']['preferences']
