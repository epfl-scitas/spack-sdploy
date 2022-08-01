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

from pdb import set_trace as st

from collections.abc import MutableMapping
from copy import deepcopy
import inspect

from .yaml_manager import ReadYaml


class PackagesYaml(ReadYaml):
    """Manage the packages section in stack.yaml"""

    def __init__(self, platform_file, stack_file, debug):
        """Declare class structs"""

        # Used to create packages.yaml:
        self.defaults = {}
        self.external = {}
        # Configuration files
        self.platform_file = platform_file
        self.stack_file = stack_file
        self.debug = debug
        # Original data
        self.data = {} # The original data 
        self.stack = {} # The data grouped by `section = packages`
        # Tokens are set in yaml_manager
        self.filters = {}

        # Read stack.yaml into self.data attribute
        self.read(self.stack_file)

        # Replace tokens
        self.replace_tokens(self.data)

        # Groups entries whose section = <section> in self.stack
        self.stack = self.group_sections(deepcopy(self.data), 'packages')

        # Read filters
        self.filters = self.read_filters(self.platform_file)

    def packages_yaml_packages(self):
        """Creates a sub-dictionary containing the packages and their specs that
        will be given to jinja2 template.

            pkgs_yaml_pkgs - this dict
        """

        if self.debug:
            print(f'Entering function: {inspect.stack()[0][3]}')

        for pkg_list_name, pkg_list_cfg in self.stack.items():
            if self.debug:
                print(f'Entering package list: {pkg_list_name}')

            for pkg_list in pkg_list_cfg.get('packages'):

                if isinstance(pkg_list, dict):
                    for pkg_name, pkg_attributes in pkg_list.items():

                        if self.debug:
                            print(f'Reading package: {pkg_name}')

                        if not 'default' in pkg_attributes:
                            continue

                        self.defaults[pkg_name] = {}
                        defaults = pkg_attributes.get('default')

                        if 'version' in defaults:
                            self._packages_yaml_packages_version(pkg_name,
                                                                 defaults.get('version'))

                        if 'variants' in defaults:
                            self._packages_yaml_packages_variants(pkg_name,
                                                                  defaults.get('variants'))

    def _packages_yaml_packages_version(self, pkg_name, version_attributes):
        """Adds version to dictionary"""

        version = []
        if isinstance(version_attributes, dict):

            # Check for filters presence
            for filter in self.filters.keys():
                if filter in version_attributes:
                    version.append(version_attributes.get(filter).get(self.filters.get(filter)))

        # We are just checking that version_attributes is not a structure (dict, list, etc)
        if not isinstance(version_attributes, dict):
            # We need to cast version to str because of ' '.join in next step
            version.append(str(version_attributes))

        if version:
            self.defaults[pkg_name]['version'] = ' '.join(version)

    def _packages_yaml_packages_variants(self, pkg_name, variants_attributes):
        """Adds variants to dictionary"""

        variants = []
        if 'common' in variants_attributes:
            variants.append(variants_attributes.get('common'))

        if isinstance(variants_attributes, dict):

            # Check for filters presence
            for filter in self.filters.keys():
                if filter in variants_attributes:
                    if variants_attributes.get(filter).get(self.filters.get(filter)) is not None:
                        variants.append(variants_attributes.get(filter).get(self.filters.get(filter)))
        # We are just checking that version_attributes is not a structure (dict, list, etc)
        if not isinstance(variants_attributes, dict):
            # We need to cast version to str because of ' '.join in next step
            variants.append(str(variants_attributes))

        if variants:
            self.defaults[pkg_name]['variants'] = ' '.join(variants)

    def packages_yaml_external(self):
        """Creates a sub-dictionary containing the packages and their specs that
        will be given to jinja2 template.

            pkgs_external - this dict
        """

        if self.debug:
            print(f'Entering function: {inspect.stack()[0][3]}')

        for pkg_list_name, pkg_list_cfg in self.stack.items():
            for pkg_list in pkg_list_cfg.get('packages'):
                if isinstance(pkg_list, dict):
                    for pkg_name, pkg_attributes in pkg_list.items():
                        if not 'external' in pkg_attributes:
                            continue

                        self.external[pkg_name] = pkg_attributes.get('external')
                        # externals = pkg_attributes.get('external')

