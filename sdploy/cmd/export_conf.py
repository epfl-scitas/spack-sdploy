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

description = "export common.yaml to bash script"
section = "Sdploy"
level = "short"

from ..util import *
from ..config import *

import os
import stat
from jinja2 import Environment, FileSystemLoader

def export_conf(parser, args):
    """Create environments"""

    envs_list = ReadYaml()
    envs_list.read(fs.join_path(get_prefix(), 'stacks/common.yaml'))

    common = {}
    for k,v in envs_list.data.items():
        if isinstance(v, str):
            if 'str' not in common:
                common['str'] = {}
            common['str']['SDPLOY_' + k.upper()] = v

    # Jinja setup
    file_loader = FileSystemLoader(fs.join_path(get_prefix(), 'templates'))
    jinja_env = Environment(loader = file_loader, trim_blocks = True)

    # Render and write
    template = jinja_env.get_template('common.yaml.j2')
    output = template.render(common = common)
    print(output)
    filename = 'jenkins/deploy/scripts/common_config.sh'
    with open(filename, 'w') as f:
        f.write(output)

    os.chmod(filename, 0o775)
