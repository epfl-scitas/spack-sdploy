# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
import sys
import textwrap

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.build_environment
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.fetch_strategy
import spack.monitor
import spack.paths
import spack.report
from spack.error import SpackError
from spack.installer import PackageInstaller

description = "install compilers"
section = "Sdploy"
level = "short"

from ..util import *
from ..config import *
from ..read_leafs import ReadLeaf
from ..config_manager import Config
from ..common_parser import setup_parser

from pdb import set_trace as st

def read_compilers(parser, args):
    """Returns list of comilers defined in stack"""

    config = Config(args)
    if config.debug:
        config.info()

    # Instantiate class
    compilers = ReadLeaf(config.platform_yaml, config.stack_yaml, config.debug)

    # Gather leafs from tree
    compilers.read_key('compiler')

    return(compilers.leafs)
