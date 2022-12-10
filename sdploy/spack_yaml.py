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
from collections.abc import MutableMapping
from copy import deepcopy
import inspect

import llnl.util.tty as tty
import spack.schema

from .stack_file import StackFile, FilterException
from .util import *

class SpackYaml(StackFile):
    """Manage the packages section in stack.yaml"""

    def __init__(self, config):
        """Declare class structs"""

        super().__init__(config)
        self.schema = spack.schema.env.schema

        # These variables will be used in StackFile class.
        # Each command that write an Yaml file must define these 4 variables.
        # This technique allows for individual command customization of each
        # one of these parameters and at the same time the reuse of the functions
        # all gathered in a single module.
        self.templates_path = self.config.templates_path
        self.template_file = self.config.spack_yaml_template
        self.yaml_path = self.config.spack_config_path
        self.yaml_file = self.config.spack_yaml

        # The 4 dictionaries to give to jinja. The whole
        # purpose of this class is to construct these dicts.
        self.pe_defs = {}
        self.pkgs_defs = {}
        self.pe_specs = {}
        self.pkgs_specs = {}
        self.definitions_list = []

    def create_pe_libraries_specs_dict(self):
        pass

    def create_pe_compiler_specs_dict(self):
        """Regroup compilers for parsing in specs"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        data = self.group_sections(deepcopy(self.data), 'pe')

        for pe, stack in data.items():
            for stack_name in stack.keys():
                self.pe_specs[pe + '_' + stack_name] = list(stack[stack_name].keys())
                # Remove compilers
                if 'compiler' in self.pe_specs[pe + '_' + stack_name]:
                    self.pe_specs[pe + '_' + stack_name].remove('compiler')
                if 'compiler_spec' in self.pe_specs[pe + '_' + stack_name]:
                    self.pe_specs[pe + '_' + stack_name].remove('compiler_spec')

    def create_pe_definitions_dict(self, filter = 1, core = True):
        """Regroup PE definitions in a single dictionary"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self.pe_stack = self.group_sections(deepcopy(self.data), 'pe')

        # Hack for adding core_compiler definition
        if core:
            core_compiler = self.group_sections(deepcopy(self.data), 'core')
            for k, v in core_compiler.items():
                self.pe_stack[k] = v

        # Check for filters presence and applies filters
        for pe, stack in self.pe_stack.items():
            for stack_name, stack_env in stack.items():
                for filter in self.filters.keys():
                    if filter in stack_env and isinstance(stack_env[filter], dict):
                        spec = stack_env[filter][self.filters[filter]]
                        stack_env[filter] = spec

        self.pe_defs = self._flatten_dict(self.pe_stack)

    def create_pkgs_definitions_dict(self):
        """Regroup package lists with their specs"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self.pkgs_stack = self.group_sections(deepcopy(self.data), 'packages')
        for pkg_list_name, pkg_list_cfg in self.pkgs_stack.items():

            tty.debug(f'Entering package list: {pkg_list_name}')

            self.definitions_list.append(pkg_list_name)

            self.pkgs_defs[pkg_list_name] = []
            for pkg_list in pkg_list_cfg.get('packages'):
                package = None
                # This is the case where the package has no structure
                if isinstance(pkg_list, str):
                    package = [pkg_list]
                    tty.debug(f'Reading package: {package}')

                if isinstance(pkg_list, dict):
                    package = self._handle_package_dictionary(pkg_list)

                if package:
                    self.pkgs_defs[pkg_list_name].append(((' '.join(package)).strip()))

    def create_pkgs_specs_dict(self):
        """Regroup package lists with PE components to write the matrix specs.
        pkgs_specs is the dictionary we are constructing in this method."""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self.pkgs_stack = self.group_sections(deepcopy(self.data), 'packages')
        for pkg_list_name, pkg_list_cfg in self.pkgs_stack.items():
            # Create new entry
            self.pkgs_specs[pkg_list_name] = {}
            # Add compilers
            self.pkgs_specs[pkg_list_name]['compilers'] = pkg_list_cfg.get('pe')
            # Add dependencies
            if 'dependencies' in pkg_list_cfg.keys():
                # Add dependencies one by one and check against filters
                # if dependency is equals to the string "none" in which
                # case do not add the dependency. In the end, if the
                # dependencies list is empty, remove it.
                self.pkgs_specs[pkg_list_name]['dependencies'] = []
                for d in pkg_list_cfg['dependencies']:
                    if d in self.filters.keys() and self.filters[d] != 'none':
                        self.pkgs_specs[pkg_list_name]['dependencies'].append(d)
                    elif d not in self.filters.keys():
                        self.pkgs_specs[pkg_list_name]['dependencies'].append(d)
                if len(self.pkgs_specs[pkg_list_name]['dependencies']) == 0:
                    self.pkgs_specs[pkg_list_name].pop('dependencies')

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
