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
#import spack.repo
#import spack.stage

description = "print out the location of a single spec"
section = "Sdploy"
level = "short"

from pdb import set_trace as st

def setup_parser(subparser):
    global directories
    directories = subparser.add_mutually_exclusive_group()

    directories.add_argument(
        '-i', '--install-dir', action='store_true',
        help="install prefix for spec (spec need not be installed)")

    arguments.add_common_arguments(subparser, ['spec'])


def s_location(parser, args):

    specs = spack.cmd.parse_specs(args.spec)

    if not specs:
        tty.die("You must supply a spec.")

    if len(specs) != 1:
        tty.die("Too many specs.  Supply only one.")

    # install_dir command matches against installed specs.
    if args.install_dir:
        env = ev.active_environment()
        spec = spack.cmd.disambiguate_spec(specs[0], env) # Returs the concrete spec
        print(spec.prefix)
        return

