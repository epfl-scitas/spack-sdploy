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

description = "deploy modules configuration"
section = "Sdploy"
level = "short"

# spack sdploy imports
from ..modules_yaml import ModulesYaml
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

def write_modules_yaml(parser, args):

    # spack-sdploy setup
    config = Config(args)
    if config.debug:
        config.info()

    # Instantiate ModulesYaml class
    modules = ModulesYaml(config, config.debug)

    # Write modules file
    modules.write_yaml()

    # WHAT WE ARE GOING TO DO IS TO CONSTRUCT THE `modules` DICTIONARY
    # THAT WILL IN THE END FEED THE `modules.yaml.j2` TEMPLATE.
    #
    # 1. modules['core_compiler'] (str)
    # 2. modules['lmod_roots'] (str)
    # 3. modules['tcl_roots'] (str)
    # 4. modules['tcl_roots'] (dictionary read from stack.yaml)

    # STACK.YAML
    #
    # Check for section modules:
    #                     blacklist:true
    #                     activated:true

    # Think about introducing `suffix` in stack.yaml

# modules:
#   all:
#     suffixes:
#       +mpi: mpi
#       +openmp: openmp
#       threads=openmp: openmp
#       ^fftw+openmp: openmp
#       +cuda: cuda
#       +nvptx: cuda
#       hdf5=parallel: h5
#       ^python@:2.99: py2
#     environment:
#       set:
#         ${PACKAGE}_ROOT: ${PREFIX}

