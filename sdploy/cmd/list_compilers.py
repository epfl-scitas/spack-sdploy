# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

description = "list-compilers"
section = "Sdploy"
level = "short"

from ..read_compilers import Compilers
from ..config_manager import Config
from ..common_parser import setup_parser

from pdb import set_trace as st

def list_compilers(parser, args):
    """Returns list of comilers defined in stack"""

    config = Config(args)

    # Instantiate class
    compilers = ReadCompilers(config)

    print('\n'.join(compilers.list_compilers()))
