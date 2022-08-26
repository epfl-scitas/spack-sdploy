# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
# SCITAS STACK DEPLOYMENT 2022, EPFL                                          #
#                                                                             #
# This command write the modules.yaml file. The platform argument is          #
# mandatory because it will read from the platform the core compiler.         #
#                                                                             #
# The stack is also mandatory, because it is under the stack directory        #
# that the commons.yaml file will be found as well as the platform directory. #
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
from ..common_parser import setup_parser

def write_modules_yaml(parser, args):
    """Write modules.yaml file"""

    # spack-sdploy setup
    config = Config(args)

    # Instantiate ModulesYaml class
    modules = ModulesYaml(config)

    # Write modules file.
    # Each commend must pass the dictionary in the contents variable.
    modules.write_yaml(data = modules.modules)
