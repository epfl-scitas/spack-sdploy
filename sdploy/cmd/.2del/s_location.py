# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev

# import spack.paths
# import spack.repo
# import spack.stage

from ..config_manager import Config
from ..read_leafs import ReadLeaf

description = "print out the location of a single spec"
section = "Sdploy"
level = "short"

from pdb import set_trace as st

def setup_parser(subparser):

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
   
#    global directories
#    directories = subparser.add_mutually_exclusive_group()
#
#    directories.add_argument(
#        '-i', '--install-dir', action='store_true',
#        help="install prefix for spec (spec need not be installed)")
#
#    arguments.add_common_arguments(subparser, ['spec'])


def s_location(parser, args):

    config = Config(args)
    if config.debug:
        config.info()

    # Instantiate class
    compiler_specs = ReadLeaf(config.platform_yaml, config.stack_yaml, config.debug)

    # Gather leafs from tree
    compiler_specs.read_key('compiler')

    for compiler in compiler_specs.leafs:

        args.spec = compiler
        
        # END OF SPACK-SDPLOY CODE
        # -- -- -- -- -- -- -- -- -- -- -- -- -- --

        specs = spack.cmd.parse_specs(args.spec)
        
        # install_dir command matches against installed specs.
        env = ev.active_environment()
        spec = spack.cmd.disambiguate_spec(specs[0], env) # Returs the concrete spec
        print(spec.prefix)
    

