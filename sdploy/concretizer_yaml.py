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

class ConcretizerYaml(StackFile):
    """Provides methods to write the concretizer.yaml configuration"""

    def __init__(self, config):
        """Declare class structs"""

        super().__init__(config)
        self.schema = spack.schema.concretizer.schema

        # These variables will be used in StackFile class.
        # Each command that write an Yaml file must define these 4 variables.
        # This technique allows for individual command customization of each
        # one of these parameters and at the same time the reuse of the functions
        # all gathered in a single module.
        self.templates_path = self.config.templates_path
        self.template_file = self.config.concretizer_yaml_template
        self.yaml_path = self.config.spack_config_path
        self.yaml_file = self.config.concretizer_yaml

        self.concretizer = {}
        self._create_dictionary()

    def _create_dictionary(self):
        """Populates dictionary with the values it will
        need to write the modules.yaml file"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self._read_configuration()
        self._load_configuration()

    def _read_configuration(self):
        """Read 'concretizer' section from commons.yaml"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        commons = ReadYaml()
        commons.read(os.path.join(self.config.commons_yaml))
        if 'concretizer' in commons.data.keys():
            self.config = commons.data['concretizer']

    def _load_configuration(self):
        """Add concretizer features"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self.concretizer = self.config
