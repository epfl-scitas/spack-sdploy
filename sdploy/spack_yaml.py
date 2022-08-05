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

from collections.abc import MutableMapping
from copy import deepcopy
import inspect

from .yaml_manager import ReadYaml

class FilterException(Exception):
    """Exception raised when filter evaluation fails"""
    def __init__(self, filter, filter_value):
        self.filter = filter
        self.filter_value = filter_value


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

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self.pe_stack = self.group_sections(deepcopy(self.data), 'pe')

        # Hack for adding core_compiler definition
        core_compiler = self.group_sections(deepcopy(self.data), 'core')
        for k,v in core_compiler.items():
            self.pe_stack[k] = v

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

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self.pkgs_stack = self.group_sections(deepcopy(self.data), 'packages')
        for pkg_list_name, pkg_list_cfg in self.pkgs_stack.items():

            tty.debug(f'Entering package list: {pkg_list_name}')

            self.pkgs_defs[pkg_list_name] = []
            for pkg_list in pkg_list_cfg.get('packages'):

                # This is the case where the package has no structure
                if isinstance(pkg_list, str):
                    package = [pkg_list]
                    tty.debug(f'Reading package: {package}')

                try:
                    if isinstance(pkg_list, dict):
                        for pkg_name, pkg_attributes in pkg_list.items():
                            package = [pkg_name]
                            tty.debug(f'Reading package: {package}')

                            # Do not force user to use `variants` if he only wants a filter
                            for filter in self._filters_in_package(pkg_attributes):
                                package.append(pkg_attributes[filter].get(self.filters.get(filter)))

                            for attr in ['version', 'variants', 'dependencies']:
                                if attr in pkg_attributes:
                                    _spack_yaml_pkg = getattr(SpackYaml, '_spack_yaml_pkg_' + attr)

                                    #calling self._spack_yaml_pkg_<attr>
                                    package.append(_spack_yaml_pkg(self, pkg_name, pkg_attributes[attr]))
                except FilterException as fe:
                    tty.debug(f'Ignoring package {pkg_name} due to missing value for {fe.filter_value} in filter {fe.filter}')
                    continue

                self.pkgs_defs[pkg_list_name].append(((' '.join(package)).strip()))

    def create_pkgs_specs_dict(self):
        """Regroup package lists with PE components to write the matrix specs"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

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

    def __handle_filter(self, attributes):
        result = []
        if isinstance(attributes, dict):
            # Check for filters presence
            for filter in self.filters.keys():
                if filter in attributes:
                    if self.filters[filter] in attributes[filter]:
                        values = attributes[filter][self.filters[filter]]
                        if isinstance(values, list):
                            result.extend(values)
                        else:
                            result.append(values)
                    else:
                        raise FilterException(filter, self.filters[filter])
        else: # We are just checking that attributes is not a structure (dict, list, etc)
            # We need to cast version to str because of ' '.join in next step
            result.append(str(attributes))
        return result

    def _spack_yaml_pkg_version(self, pkg_name, version_attributes):
        """Returns package version"""

        version = self.__handle_filter(version_attributes)
        return(' '.join(version))


    def _spack_yaml_pkg_variants(self, pkg_name, variants_attributes):
        """Returns package variants"""

        variants = []
        if 'common' in variants_attributes:
            variants.append(variants_attributes.get('common'))

        variants.extend(self.__handle_filter(variants_attributes))

        return(' '.join(variants))

    def _spack_yaml_pkg_dependencies(self, pkg_name, dependencies_attributes):
        """Returns package dependencies"""

        dependencies = []
        # We are just checking that version_attributes is not a structure (dict, list, etc)
        if isinstance(dependencies_attributes, list):
            dependencies = dependencies_attributes
        else:
            dependencies = self.__handle_filter(dependencies_attributes)

        return(' ^' + ' ^'.join(dependencies))

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
