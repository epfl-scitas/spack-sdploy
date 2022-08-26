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

from .yaml_manager import ReadYaml
from .util import *

class ModulesYaml(ReadYaml):
    """Provides methods to write the modules.yaml configuration"""

    def __init__(self, config):
        """Declare class structs"""

        # Configuration files
        self.config = config
        self.debug = config.debug
        self.modules = {}

        # Call method that will populate dict
        self._create_dictionary()

        self.template = config.modules_yaml_template
        self.yaml = config.modules_yaml
        self.schema = spack.schema.modules.schema

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

    def _write_yaml(self, output, filename):
        """Docstring"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        with fs.write_tmp_and_move(os.path.realpath(filename)) as f:
            yaml = syaml.load_config(output)
            # spack.config.validate(yaml, spack.schema.env.schema, filename)
            syaml.dump_config(yaml, f, default_flow_style=False)

    def write_yaml(self):
        """Write modules.yaml"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        # Jinja setup
        file_loader = FileSystemLoader(self.config.templates_path)
        jinja_env = Environment(loader = file_loader, trim_blocks = True)

        # Check that template file exists
        path = os.path.join(self.config.templates_path, self.config.modules_yaml_template)
        if not os.path.exists(path):
            tty.die(f'Template file {self.config.modules_yaml_template} does not exist ',
                    f'in {path}')

        template = jinja_env.get_template(self.config.modules_yaml_template)
        output = template.render(modules = self.modules)

        tty.msg(self.config.modules_yaml)
        print(output)

        env = ev.active_environment()
        if env:
            self._write_yaml(output, os.path.realpath(env.manifest_path))
        else:
            filename = os.path.join(self.config.spack_config_path, self.config.modules_yaml)
            tty.msg(f'Writing file {filename}')
            self._write_yaml(output, filename)

