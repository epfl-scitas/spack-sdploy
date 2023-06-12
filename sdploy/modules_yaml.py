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
import inspect
import copy

import spack
import spack.cmd
import spack.config
import spack.environment as ev
import spack.schema.env
import llnl.util.tty as tty


from .stack_file import StackFile
from .util import ReadYaml


class ModulesYaml(StackFile):
    """Provides methods to write the modules.yaml configuration"""

    def __init__(self, config):
        """Declare class structs"""

        super().__init__(config)
        self.schema = spack.schema.modules.schema

        # These variables will be used in StackFile class.
        # Each command that write an Yaml file must define these 4 variables.
        # This technique allows for individual command customization of each
        # one of these parameters and at the same time the reuse of the functions
        # all gathered in a single module.
        self.templates_path = self.config.templates_path
        self.template_file = self.config.modules_yaml_template
        self.yaml_path = self.config.spack_config_path
        self.yaml_file = self.config.modules_yaml

        self.commons = ReadYaml()
        self.commons.read(os.path.join(self.config.commons_yaml))

        self.modules = {}
        self._create_dictionary()

    def _create_dictionary(self):
        """Populates dictionary with the values it will
        need to write the modules.yaml file"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self._add_core_compiler()
        self._add_module_roots()
        self._add_suffixes()

    def _add_core_compiler(self):
        """Add core compiler to the modules dictionary"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        platform = ReadYaml()
        platform.read(os.path.join(self.config.platform_yaml))
        self.modules['core_compiler'] = self.tokens['core_compiler']

    def _add_module_roots(self):
        """Add modules installation paths. Note that These
        are read from commons.yaml and not from sdploy.yaml."""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        modules = self.config.configs["modules"]

        for module_type in ['lmod', 'tcl']:
            self.modules[f'{module_type}_roots'] = modules[f'{module_type}_roots']

    def _add_suffixes(self):
        """Add modules suffixes from stack.yaml"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        if ('modules' not in self.commons.data or
            'suffixes' not in self.commons.data['modules']):
            return

        self.modules['suffixes'] = copy.copy(
            self.commons.data['modules']['suffixes'])
