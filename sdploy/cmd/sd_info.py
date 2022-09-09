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

description = "show spack-sdploy configuration"
section = "Sdploy"
level = "short"

# spack sdploy imports
from ..util import *
from ..config import *
from ..config_manager import Config

def setup_parser(subparser):
    # spack-sdploy will look for a stack after the name given in the parameter
    # stack under the stacks directory. If it doesn't find, it will assume that
    # the parameter stack is a fully qualified file name to a stack.yaml file.
    subparser.add_argument(
        '-s', '--stack',
        help='name of the stack.'
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

def sd_info(parser, args):

    #st()
    # spack-sdploy setup
    config = Config(args)
    config.info()
