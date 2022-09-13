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

description = "deploy concretizer configuration"
section = "Sdploy"
level = "short"

# spack sdploy imports
from ..concretizer_yaml import ConcretizerYaml
from ..util import *
from ..config import *
from ..config_manager import Config
from ..common_parser import setup_parser

def write_concretizer_yaml(parser, args):
    """Write modules.yaml file"""

    # spack-sdploy setup
    config = Config(args)

    # Instantiate ConcretizerYaml class
    concretizer = ConcretizerYaml(config)

    # Write concretizer file.
    # Each commend must pass the dictionary in the contents variable.

    data = concretizer.concretizer
    concretizer.write_yaml(data = concretizer.concretizer)
