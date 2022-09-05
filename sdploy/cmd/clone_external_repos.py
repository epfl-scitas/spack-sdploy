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

description = "clone-extrnal-repos"
section = "Sdploy"
level = "short"

# spack sdploy imports
from ..repos_yaml import ReposYaml
from ..util import *
from ..config import *
from ..config_manager import Config
from ..common_parser import setup_parser

def clone_external_repos(parser, args):

    # spack-sdploy setup
    config = Config(args)

    # Instantiate ModulesYaml class
    repos = ReposYaml(config)

    # Clone the repositories
    repos.clone()    
