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
import spack
import spack.cmd
import spack.config
import spack.environment as ev
import spack.schema.env
import spack.util.spack_yaml as syaml
import llnl.util.filesystem as fs
import llnl.util.tty as tty

from jinja2 import Environment, FileSystemLoader

description = "write packages.yaml file"
section = "Sdploy"
level = "short"

from ..packages_yaml import PackagesYaml
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
        spack.config.validate(yaml, spack.schema.packages.schema, filename)
        syaml.dump_config(yaml, f, default_flow_style=False)


def write_packages_yaml(parser, args):
    """Create spack.yaml file"""

    config = Config(args)
    if config.debug:
        config.info()

    # Initiates variables and does initial processing
    pkgs = PackagesYaml(config.platform_yaml, config.stack_yaml, config.debug)

    # Create default packages dictionary
    pkgs.packages_yaml_packages()

    # Create external packages dictionary
    pkgs.packages_yaml_external()

    # Group dictionaries together. Further dictionaries can be added later
    # if new features are needed.
    data = {}
    data['defaults'] = pkgs.defaults
    data['externals'] = pkgs.externals

    # Set up jinja
    file_loader = FileSystemLoader(config.templates_path)
    jinja2_env = Environment(loader = file_loader, trim_blocks = True)

    # Render and write packages.yaml
    template = jinja2_env.get_template(config.packages_yaml_template)
    output = template.render(packages = data)

    tty.msg(output)

    env = ev.active_environment()
    if env:
        filename = os.path.join(os.path.dirname(os.path.realpath(env.manifest_path)),
                                'packages.yaml')
        _write_yaml(output, filename)
    else:
        _write_yaml(output, packages_yaml)
