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

def create_environments(parser, args):
    """Create environments"""

    envs_list = ReadYaml()
    envs_list.read(fs.join_path(get_prefix(), 'stacks/common.yaml'))

    for e in envs_list.data['environments']:
        if e not in ev.all_environment_names():
            tty.info(f'Environment {e} not found')
            _env_create(e)
