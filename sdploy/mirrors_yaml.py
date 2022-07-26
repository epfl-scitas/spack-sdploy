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


from .stack_file import StackFile
from .util import *

class MirrorsYaml(StackFile):
    """Provides methods to write the modules.yaml configuration"""

    def __init__(self, config):
        """Declare class structs"""

        super().__init__(config)
        self.schema = spack.schema.mirrors.schema

        # These variables will be used in StackFile class.
        # Each command that write an Yaml file must define these 4 variables.
        # This technique allows for individual command customization of each
        # one of these parameters and at the same time the reuse of the functions
        # all gathered in a single module.
        self.templates_path = self.config.templates_path
        self.template_file = self.config.mirrors_yaml_template
        self.yaml_path = self.config.spack_config_path
        self.yaml_file = self.config.mirrors_yaml

        self.common = ReadYaml()
        self.common.read(self.config.commons_yaml)

        self.mirrors = {}
        self._create_dictionary()

    def _create_dictionary(self):
        """Populates dictionary with the values it will
        need to write the mirrors.yaml file"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        self._add_mirrors_list()

    def _add_mirrors_list(self):
        """Add mirrors installation paths. Note that These
        are read from commons.yaml and not from sdploy.yaml."""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        self.mirrors['paths'] = {}
        for mirror, path in self.common.data['mirrors'].items():
            self.mirrors['paths'][mirror] = os.path.join(
                self.common.data['work_directory'],
                path)
