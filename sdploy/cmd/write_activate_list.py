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

description = "write list of packages to activate"
section = "Sdploy"
level = "short"

# spack sdploy imports
from ..activate_pkgs import ActivatePkgs
from ..util import *
from ..config import *
from ..config_manager import Config
from ..common_parser import setup_parser

def write_activate_list(parser, args):

    # spack-sdploy setup
    config = Config(args)

    # Instantiate class
    pkgs = ActivatePkgs(config)

    # Write list
    pkgs.write_activated_pkgs()
