from pdb import set_trace as st

from collections.abc import MutableMapping
from copy import deepcopy
import inspect

from .yaml_manager import ReadYaml

class SpackYaml(ReadYaml):
    """Manage the packages section in stack.yaml"""

    def __init__(self, platform_file, stack_file, debug):
        """Declare class structs"""

        # The 4 dictionaries to give to jinja. The whole
        # purpose of this class is to construct these dicts.
        self.pe_defs = {}
        self.pkgs_defs = {}
        self.pe_specs = {}
        self.pkgs_specs = {}

        # Configuration
        self.platform_file = platform_file
        self.stack_file = stack_file
        self.debug = debug

        # Original data
        self.data = {}

        # Filters
        self.filters = {}

        # Read stack.yaml into self.data attribute
        self.read(self.stack_file)

        # Replace tokens
        self.replace_tokens(self.data)

        # Read filters from platform file
        self.filters = self.read_filters(self.platform_file)

    def create_pe_libraries_specs_dict(self):
        pass

    def create_pe_compiler_specs_dict(self):
        """Regroup compilers for parsing in specs"""

        if self.debug:
            print(f'Entering function: {inspect.stack()[0][3]}')

        data = self.group_sections(deepcopy(self.data), 'pe')

        for pe, stack in data.items():
            for stack_name in stack.keys():
                self.pe_specs[pe + '_' + stack_name] = list(data.get(pe).get(stack_name).keys())
                # compiler is defined by default
                self.pe_specs[pe + '_' + stack_name].pop(0)

    def create_pe_definitions_dict(self, filter = 1):
        """Regroup PE definitions in a single dictionary"""

        if self.debug:
            print(f'Entering function: {inspect.stack()[0][3]}')

        self.pe_stack = self.group_sections(deepcopy(self.data), 'pe')

        # Check for filters presence and applies filters
        for pe, stack in self.pe_stack.items():
            for stack_name, stack_env in stack.items():
                for filter in self.filters.keys():
                    if (filter in stack_env
                       and isinstance(self.pe_stack.get(pe).get(stack_name).get(filter), dict)):

                        spec = self.pe_stack.get(pe).get(stack_name).get(filter) \
                                .get(self.filters.get(filter))
                        self.pe_stack[pe][stack_name][filter] = spec

        self.pe_defs = self._flatten_dict(self.pe_stack)

    def create_pkgs_definitions_dict(self):
        """Regroup package lists with their specs"""

        if self.debug:
            print(f'Entering function: {inspect.stack()[0][3]}')

        self.pkgs_stack = self.group_sections(deepcopy(self.data), 'packages')
        for pkg_list_name, pkg_list_cfg in self.pkgs_stack.items():

            if self.debug:
                print(f'Entering package list: {pkg_list_name}')

            self.pkgs_defs[pkg_list_name] = []
            for pkg_list in pkg_list_cfg.get('packages'):

                # This is the case where the package has no structure
                if isinstance(pkg_list, str):
                    package = [pkg_list]
                    if self.debug:
                        print(f'Reading package: {package}')

                if isinstance(pkg_list, dict):
                    for pkg_name, pkg_attributes in pkg_list.items():
                        package = [pkg_name]
                        if self.debug:
                            print(f'Reading package: {package}')

                        # Do not force user to use `variants` if he only wants a filter
                        for filter in self._filters_in_package(pkg_attributes):
                            package.append(pkg_attributes[filter].get(self.filters.get(filter)))

                        if 'version' in pkg_attributes:
                            package.append(
                                self._spack_yaml_pkg_version(
                                    pkg_name, pkg_attributes.get('version'))
                            )

                        if 'variants' in pkg_attributes:
                            package.append(
                                self._spack_yaml_pkg_variants(
                                    pkg_name, pkg_attributes.get('variants'))
                            )

                        if 'dependencies' in pkg_attributes:
                            package.append(
                                self._spack_yaml_pkg_dependencies(
                                    pkg_name, pkg_attributes.get('dependencies'))
                            )

                # VERY UGLY THING TO REMOVE VERY SOON
                EXCLUDE_PACKAGE = False
                for item in package:
                    if 'EXCLUDE_PACKAGE' in item:
                        EXCLUDE_PACKAGE = True
                if EXCLUDE_PACKAGE:
                    continue

                self.pkgs_defs[pkg_list_name].append(((' '.join(package)).strip()))

    def create_pkgs_specs_dict(self):
        """Regroup package lists with PE components to write the matrix specs"""

        if self.debug:
            print(f'Entering function: {inspect.stack()[0][3]}')

        self.pkgs_stack = self.group_sections(deepcopy(self.data), 'packages')
        for pkg_list_name, pkg_list_cfg in self.pkgs_stack.items():
            self.pkgs_specs[pkg_list_name] = {}
            self.pkgs_specs[pkg_list_name]['compilers'] = pkg_list_cfg.get('pe')
            if 'dependencies' in pkg_list_cfg.keys():
                self.pkgs_specs[pkg_list_name]['dependencies'] = pkg_list_cfg.get('dependencies')

    def _filters_in_package(self, dic):
        """Return list of filters found in dictionary"""

        result = []
        for filter in self.filters.keys():
            if filter in dic:
                result.append(filter)
        return(result)

    def _spack_yaml_pkg_version(self, pkg_name, version_attributes):
        """Returns package version"""

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

        return(' '.join(version))

    def _spack_yaml_pkg_variants(self, pkg_name, variants_attributes):
        """Returns package variants"""

        variants = []
        if 'common' in variants_attributes:
            variants.append(variants_attributes.get('common'))

        if isinstance(variants_attributes, dict):

            # Check for filters presence
            for filter in self.filters.keys():
                if filter in variants_attributes:

                    if variants_attributes.get(filter).get(self.filters.get(filter)) is not None:
                        variants.append(variants_attributes.get(filter).get(self.filters.get(filter)))
                    # VERY UGLY THING TO REMOVE VERY SOON
                    if variants_attributes.get(filter).get(self.filters.get(filter)) is None:
                        variants.append('EXCLUDE_PACKAGE')

        # We are just checking that version_attributes is not a structure (dict, list, etc)
        if not isinstance(variants_attributes, dict):
            # We need to cast version to str because of ' '.join in next step
            variants.append(str(variants_attributes))

        return(' '.join(variants))

    def _spack_yaml_pkg_dependencies(self, pkg_name, dependencies_attributes):
        """Returns package dependencies"""

        dependencies = []
        if isinstance(dependencies_attributes, dict):

            # Check for filters presence
            for filter in self.filters.keys():
                if filter in dependencies_attributes:

                    if dependencies_attributes.get(filter).get(self.filters.get(filter)) is not None:
                        dependencies.append(dependencies_attributes.get(filter)
                                            .get(self.filters.get(filter)))
                    # VERY UGLY THING TO REMOVE VERY SOON
                    if dependencies_attributes.get(filter).get(self.filters.get(filter)) is None:
                        dependencies.append('EXCLUDE_PACKAGE')

        # We are just checking that version_attributes is not a structure (dict, list, etc)
        if isinstance(dependencies_attributes, list):
            for d in dependencies_attributes:
                dependencies.append(str('^' + d))

        return(' '.join(dependencies))

    def _flatten_dict(self, d: MutableMapping, parent_key: str = '', sep: str = '_'):
        """Returns a flat dict

        Return a 1-depth dict (flat) whose elements are formed by composing
        the nested dicts nodes using the separator sep.
        {'a':1, 'b':{'c':2}} -> {'a':1, 'b_c':2}
        origin: freecodecamp.org"""

        return dict(self._flatten_dict_gen(d, parent_key, sep))

    def _flatten_dict_gen(self, d, parent_key, sep):

        for k, v in d.items():
            new_key = parent_key + sep + str(k) if parent_key else k
            if isinstance(v, MutableMapping):
                yield from self._flatten_dict(v, new_key, sep=sep).items()
            else:
                yield new_key, v

    # METHOD IS NOT CURRENTLY USED
    def _get_pe_list(self):
        """Return list with PE names"""

        stack = self.group_sections(deepcopy(self.data), 'pe')
        pe_list = list(stack.keys())
        if 'metadata' in pe_list:
                pe_list.pop('metadata')

        return(pe_list)
