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
from spack.cmd.env import _env_create

description = "create environments"
section = "Sdploy"
level = "short"

from ..util import *
from ..config import *
from ..config_manager import Config

def setup_parser(subparser):
    # spack-sdploy will look for a stack after the name given in the parameter
    # stack under the stacks directory. If it doesn't find, it will assume that
    # the parameter stack is a fully qualified file name to a stack.yaml file.
    subparser.add_argument(
        '-s', '--stack',
        help='path to the stack file'
    )
    subparser.add_argument(
        '-p', '--platform',
        help='path to the platform file.'
    )
    subparser.add_argument(
        '--prefix', type=str,
        help='path to the stacks directory.'
    )
    subparser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='print debug information.'
    )

def create_environments(parser, args):
    """Create environments"""

    # spack-sdploy setup
    config = Config(args)
    if config.debug:
        config.info()

    envs_list = ReadYaml()
    envs_list.read(fs.join_path(config.commons_yaml))

    tty.info(f'The following environments were found in commons.yaml:')
    for e in envs_list.data['environments']:
        print(f'- {e}')

    for e in envs_list.data['environments']:
        if e not in ev.all_environment_names():
            tty.info(f'Environment {e} not found in spack.')
            _env_create(e)
        else:
            tty.info(f'Environment {e} already exists in spack, passing.')
