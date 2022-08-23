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

description = "deploy config.yaml file"
section = "Sdploy"
level = "short"

# spack sdploy imports
from ..config_yaml import ConfigYaml
from ..util import *
from ..config import *
from ..config_manager import Config
from ..common_parser import setup_parser

def write_config_yaml(parser, args):

    st()
    # spack-sdploy setup
    config = Config(args)
    if config.debug:
        config.info()

#    # Instantiate ConfigYaml class
#    conf = ConfigYaml(config, config.debug)
#
#    # Write modules file
#    conf.write_yaml()
