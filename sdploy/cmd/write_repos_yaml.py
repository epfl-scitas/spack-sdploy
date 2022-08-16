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

import spack
import spack.cmd
import spack.config
import spack.environment as ev
import spack.schema.env
import spack.util.spack_yaml as syaml
import llnl.util.filesystem as fs
import llnl.util.tty as tty

from jinja2 import Environment, FileSystemLoader

description = "write spack.yaml file"
section = "Sdploy"
level = "short"

from ..spack_yaml import SpackYaml
from ..util import *
from ..config import *
from ..config_manager import Config

def setup_parser(subparser):
    subparser.add_argument(
        '-s', '--stack',
        help='path to the stack file'
    )
    subparser.add_argument(
        '-p', '--platform',
        help='path to the platform file.'
    )
    subparser.add_argument(
        '-t', '--templates-path',
        help='where to find jinja templates'
    )
    subparser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='print debug information.'
    )

def _write_yaml(output, filename):
    with fs.write_tmp_and_move(os.path.realpath(filename)) as f:
        yaml = syaml.load_config(output)
        spack.config.validate(yaml, spack.schema.env.schema, filename)
        syaml.dump_config(yaml, f, default_flow_style=False)


def write_repos_yaml(parser, args):
    """Create spack.yaml file"""

    config = Config(args)
    if config.debug:
        config.info()


    read_configuration()

    create_diectories()

    clone_repos()

    # Jinja setup
    file_loader = FileSystemLoader(config.templates_path)

    jinja_env = Environment(loader = file_loader, trim_blocks = True)

    # Render and write spack.yaml
    template = jinja_env.get_template(config.spack_yaml_template)
    output = template.render(stack = data)

    tty.msg(config.spack_yaml)
    print(output)

    env = ev.active_environment()
    if env:
        _write_yaml(output, os.path.realpath(env.manifest_path))
    else:
        _write_yaml(output, config.spack_yaml)
