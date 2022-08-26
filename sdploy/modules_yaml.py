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
import shutil
import inspect

import spack
import spack.cmd
import spack.config
import spack.environment as ev
import spack.schema.env
import spack.util.spack_yaml as syaml
import llnl.util.filesystem as fs
import llnl.util.tty as tty

from llnl.util.filesystem import mkdirp, working_dir
from spack.util.executable import ProcessError, which
from jinja2 import Environment, FileSystemLoader

from .stack_file import StackFile
from .util import *

class ModulesYaml(StackFile):
    """Provides methods to write the modules.yaml configuration"""

    def __init__(self, config):
        """Declare class structs"""

        super().__init__(config)

        # These variables will be used in StackFile class.
        # Each command that write an Yaml file must define these 4 variables.
        # This technique allows for individual command customization of each
        # one of these parameters and at the same time the reuse of the functions
        # all gathered in a single module.
        self.templates_path = self.config.templates_path
        self.template_file = self.config.modules_yaml_template
        self.yaml_path = self.config.spack_config_path
        self.yaml_file = self.config.modules_yaml

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
        self.modules['core_compiler'] = platform.data['platform']['tokens']['core_compiler']

    def _add_module_roots(self):
        """Add modules installation paths. Note that These
        are read from commons.yaml and not from sdploy.yaml."""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        commons = ReadYaml()
        commons.read(os.path.join(self.config.commons_yaml))
        self.modules['lmod_roots'] = (commons.data['work_directory'] + os.path.sep
                                      + commons.data['stack_release'] + os.path.sep
                                      + commons.data['stack_version'] + os.path.sep
                                      + commons.data['lmod_roots'])
        self.modules['tcl_roots'] = (commons.data['work_directory'] + os.path.sep
                                      + commons.data['stack_release'] + os.path.sep
                                      + commons.data['stack_version'] + os.path.sep
                                      + commons.data['tcl_roots'])

    def _add_suffixes(self):
        """Add modules suffixes from stack.yaml"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        self.modules['suffixes'] = {'+mpi': 'mpi', '+openmp': 'openmp'}

