# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
# SCITAS STACK DEPLOYMENT 2022, EPFL                                          #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, working_dir

import spack.paths
from spack.util.executable import ProcessError, which

_SPACK_UPSTREAM = 'https://github.com/spack/spack'

description = "install external repositories"
section = "Sdploy"
level = "short"

# spack sdploy imports
from pdb import set_trace as st

from ..repos_yaml import ReposYaml
from ..util import *
from ..config import *
from ..config_manager import Config
from ..common_parser import setup_parser

#def setup_parser(subparser):
#    subparser.add_argument(
#        '-s', '--stack',
#        help='name of the stack.'
#    )
#    subparser.add_argument(
#        '-p', '--platform',
#        help='name of the platform.'
#    )
#    subparser.add_argument(
#        '--prefix', type=str,
#        help='path to the stacks directory.'
#    )
#    subparser.add_argument(
#        '-d', '--debug', action='store_true', default=False,
#        help='print debug information.'
#    )

def get_origin_info(remote):
    git_dir = os.path.join(spack.paths.prefix, '.git')
    git = which('git', required=True)
    try:
        branch = git('symbolic-ref', '--short', 'HEAD', output=str)
    except ProcessError:
        branch = 'develop'
        tty.warn('No branch found; using default branch: %s' % branch)
    if remote == 'origin' and \
       branch not in ('master', 'develop'):
        branch = 'develop'
        tty.warn('Unknown branch found; using default branch: %s' % branch)
    try:
        origin_url = git(
            '--git-dir=%s' % git_dir,
            'config', '--get', 'remote.%s.url' % remote,
            output=str)
    except ProcessError:
        origin_url = _SPACK_UPSTREAM
        tty.warn('No git repository found; '
                 'using default upstream URL: %s' % origin_url)
    return (origin_url.strip(), branch.strip())


def write_repos_yaml(parser, args):

    # spack-sdploy setup
    config = Config(args)
    if config.debug:
        config.info()

    # <!> CAVEATS <!>
    # In this particular case, stack_yaml is the name of the stack and not the
    # fully qualified name of the stack.yaml file. This will be the standard
    # behaviour in future developments.

    repos = ReposYaml(config)

    repos.clone()

    repos.write_yaml()