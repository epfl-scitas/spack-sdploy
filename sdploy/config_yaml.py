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

class ConfigYaml(StackFile):
    """Provides methods to write the modules.yaml configuration"""

    def __init__(self, config):
        """Declare class structs"""

        super().__init__(config)
        self.schema = spack.schema.config.schema

        # These variables will be used in StackFile class.
        # Each command that write an Yaml file must define these 4 variables.
        # This technique allows for individual command customization of each
        # one of these parameters and at the same time the reuse of the functions
        # all gathered in a single module.
        self.templates_path = self.config.templates_path
        self.template_file = self.config.config_yaml_template
        self.yaml_path = self.config.spack_config_path
        self.yaml_file = self.config.config_yaml

        self.commons = ReadYaml()
        self.commons.read(os.path.join(self.config.commons_yaml))

        # Configuration files
        self.conf = {}

        # Call method that will populate dict
        self._create_dictionary()


    def _create_dictionary(self):
        """Populates dictionary with the values it will
        need to write the modules.yaml file"""

        self._add_license_dir()
        self._add_build_stage()
        self._add_module_roots()
        self._add_extensions()
        self._add_install_paths()

    def _add_license_dir(self):
        self.conf['license_dir'] = os.path.join(self.commons.data['work_directory'],
                                                self.commons.data['stack_release'],
                                                self.commons.data['spack_sdploy'],
                                                'external', 'licenses')       

    def _add_build_stage(self):
        """Add build stages section to the dictionary"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self.conf['build_stage'] = [
            os.path.join('$tempdir', '$user',
                         self.config.stack + '.' + self.config.stack_ver, 'tmp'),
            os.path.join('$tempdir', '$user', 'spack-stage'),
            os.path.join('~', '.spack', 'stage')
        ]

    def _add_extensions(self):
        """Add extensions to the dictionary"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self.conf['extensions'] = [
            os.path.join(self.commons.data['work_directory'],
                         self.commons.data['stack_release'],
                         self.commons.data['spack_sdploy'])
        ]

    def _add_module_roots(self):
        """Add modules installation paths"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self.conf['module_roots'] = {}
        self.conf['module_roots']['lmod'] = os.path.join(
            self.commons.data['work_directory'], 
            self.commons.data['stack_release'],
            self.commons.data['stack_version'],
            self.commons.data['lmod_roots'])
        self.conf['module_roots']['tcl'] = os.path.join(
            self.commons.data['work_directory'],
            self.commons.data['stack_release'],
            self.commons.data['stack_version'],
            self.commons.data['tcl_roots'])

    def _add_install_paths(self):
        """Add modules installation paths"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        self.conf['install_tree'] = os.path.join(
            self.commons.data['work_directory'],
            self.commons.data['stack_release'],
            self.commons.data['stack_version'],
            'opt', 'spack')
