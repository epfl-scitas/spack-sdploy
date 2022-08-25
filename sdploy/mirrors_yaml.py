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

        self.template = self.config.mirrors_yaml_template
        self.output_yaml = self.config.mirrors_yaml

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
        commons = ReadYaml()
        commons.read(self.config.commons_yaml)

        self.mirrors['paths'] = {}
        for k,v in commons.data['mirrors'].items():
            self.mirrors['paths'][k] = (commons.data['work_directory'] + os.path.sep
                                        + v)
