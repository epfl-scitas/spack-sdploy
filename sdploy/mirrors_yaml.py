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

class MirrorsYaml(ReadYaml):
    """Provides methods to write the modules.yaml configuration"""

    def __init__(self, config):
        """Declare class structs"""

        self.config = config
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
        path = os.path.join(self.config.templates_path, self.config.mirrors_yaml_template)
        if not os.path.exists(path):
            tty.die(f'Template file {self.config.mirrors_yaml_template} does not exist ',
                    f'in {path}')

        template = jinja_env.get_template(self.config.mirrors_yaml_template)
        output = template.render(mirrors = self.mirrors)

        tty.msg(self.config.mirrors_yaml)
        print(output)

        env = ev.active_environment()
        if env:
            self._write_yaml(output, os.path.realpath(env.manifest_path))
        else:
            filename = os.path.join(self.config.spack_config_path, self.config.mirrors_yaml)
            tty.msg(f'Writing file {filename}')
            self._write_yaml(output, filename)

