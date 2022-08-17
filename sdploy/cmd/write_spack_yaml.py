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
from ..util import st
from ..config import *
from ..config_manager import Config

def setup_parser(subparser):
    subparser.add_argument(
        '-s', '--stack',
        help='name of the stack to install.'
    )
    subparser.add_argument(
        '-p', '--platform',
        help='name of the platform.'
    )
    subparser.add_argument(
        '--prefix', type=str,
        help='path to the stacks directory.'
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


def write_spack_yaml(parser, args):
    """Create spack.yaml file"""

    config = Config(args)
    if config.debug:
        config.info()

    # Process Programming Environment section.
    stack = SpackYaml(config.platform_yaml, config.stack_yaml, config.debug)

    # Create PE definitions dictionary
    stack.create_pe_definitions_dict()

    # Create packages definitions dictionary
    stack.create_pkgs_definitions_dict()

    # Create PE matrix dictionary
    stack.create_pe_compiler_specs_dict()

    # Create PE support libraries matrix dictionary
    stack.create_pe_libraries_specs_dict()

    # Create package lists matrix dictionary
    stack.create_pkgs_specs_dict()

    # Concatenate all dicts
    data = {}
    data['pe_defs'] = stack.pe_defs
    data['pkgs_defs'] = stack.pkgs_defs
    data['pe_specs'] = stack.pe_specs
    data['pkgs_specs'] = stack.pkgs_specs

    # Jinja setup
    file_loader = FileSystemLoader(config.templates_path)

    jinja_env = Environment(loader = file_loader, trim_blocks = True)

    # Render and write spack.yaml
    template = jinja_env.get_template(config.spack_yaml_template)
    output = template.render(stack = data)

    tty.msg(config.spack_yaml)
    print(output)

    st()
    env = ev.active_environment()
    if env:
        _write_yaml(output, os.path.realpath(env.manifest_path))
    else:
        _write_yaml(output, config.spack_yaml)
