# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import sys

from six import iteritems

import llnl.util.tty as tty
from llnl.util.lang import index_by
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize

import spack.compilers
import spack.config
import spack.spec

description = "add compiler"
section = "Sdploy"
level = "short"

from pdb import set_trace as st

def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='compiler_command')

    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    # Find
    find_parser = sp.add_parser(
        'find', aliases=['add'],
        help='search the system for compilers to add to Spack configuration')
    find_parser.add_argument('add_paths', nargs=argparse.REMAINDER)
    find_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope('compilers'),
        help="configuration scope to modify")

def s_compiler(args):
    """Search either $PATH or a list of paths OR MODULES for compilers and
       add them to Spack's configuration.

    """

    st()
    # None signals spack.compiler.find_compilers to use its default logic
    paths = args.add_paths or None

    # Below scope=None because we want new compilers that don't appear
    # in any other configuration.
    new_compilers = spack.compilers.find_new_compilers(paths, scope=None)
    if new_compilers:
        spack.compilers.add_compilers_to_config(
            new_compilers, scope=args.scope, init_config=False
        )
        n = len(new_compilers)
        s = 's' if n > 1 else ''

        config = spack.config.config
        filename = config.get_config_filename(args.scope, 'compilers')
        tty.msg("Added %d new compiler%s to %s" % (n, s, filename))
        colify(reversed(sorted(c.spec for c in new_compilers)), indent=4)
    else:
        tty.msg("Found no new compilers")
    tty.msg("Compilers are defined in the following files:")
    colify(spack.compilers.compiler_config_files(), indent=4)

