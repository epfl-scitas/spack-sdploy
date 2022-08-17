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

def setup_parser(subparser):

    # Default spack-sdploy arguments

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
        '-t', '--templates-path',
        help='where to find jinja templates'
    )
    subparser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='print debug information.'
    )

    # spack clone.py standard arguments
#     subparser.add_argument(
#         '-r', '--remote', action='store', dest='remote',
#         help="name of the remote to clone from", default='origin')
#     subparser.add_argument(
#         'prefix',
#         help="name of prefix where we should install spack")


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


def repos_yaml(parser, args):

    # spack-sdploy setup
    config = Config(args)
    if config.debug:
        config.info()

    st()
    # <!> CAVEATS <!>
    # In this particular case, stack_yaml is the name of the stack and not the
    # fully qualified name of the stack.yaml file. This will be the standard
    # behaviour in future developments.

    repos = ReposYaml(config)

    repos.clone()

    repos.write_yaml()
