# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

description = "readc"
section = "Sdploy"
level = "short"

from ..util import *
from ..config import *
from ..read_leafs import ReadLeaf
from ..config_manager import Config
from ..common_parser import setup_parser

def readc(parser, args):
    """Return list of compilers specs as defined in stack"""

    # spack-sdploy setup
    config = Config(args)

    # Instantiate ReadLeaf class
    compilers = ReadLeaf(config)

    # Gather leafs from tree
    compilers.read_key('compiler')

    # Display results
    compilers.report_leafs()

    # Write compiler to file
    compilers.write_to_file('compilers')
