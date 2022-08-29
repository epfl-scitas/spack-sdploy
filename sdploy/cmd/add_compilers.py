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

import spack.cmd
import spack.environment as ev
import spack.compilers
import spack.config
import spack.spec

from ..config_manager import Config
from ..read_leafs import ReadLeaf

description = "add my compiler"
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

    find_parser.add_argument(
        '-s', '--stack',
        help='path to the stack file'
    )
    find_parser.add_argument(
        '-p', '--platform',
        help='path to the platform file.'
    )
    find_parser.add_argument(
        '--prefix', type=str,
        help='path to the stacks directory.'
    )
    find_parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='print debug information.'
   )


def compiler_find(args):
    """Search either $PATH or a list of paths OR MODULES for compilers and
       add them to Spack's configuration.

    """

   # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --             
   # START OF SPACK-SDPLOY CODE
   # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --             

    tty.debug(f'Reading configuration')
    config = Config(args)
    if config.debug:
        config.info()

    # Instantiate class
    compiler_specs = ReadLeaf(config.platform_yaml, config.stack_yaml, config.debug)

    # Gather leafs from tree
    tty.debug(f'Gathering compilers from stack file')
    compiler_specs.read_key('compiler')
    compiler_specs.report_leafs()

    paths = []
    for compiler in compiler_specs.leafs:
        specs = spack.cmd.parse_specs(compiler)
        env = ev.active_environment()
        spec = spack.cmd.disambiguate_spec(specs[0], env) # Returs the concrete spec
        paths.append(spec.prefix)

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --             
    # END OF SPACK-SDPLOY CODE
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --             

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


def compiler_remove(args):
    cspec = spack.spec.CompilerSpec(args.compiler_spec)
    compilers = spack.compilers.compilers_for_spec(cspec, scope=args.scope)
    if not compilers:
        tty.die("No compilers match spec %s" % cspec)
    elif not args.all and len(compilers) > 1:
        tty.error("Multiple compilers match spec %s. Choose one:" % cspec)
        colify(reversed(sorted([c.spec for c in compilers])), indent=4)
        tty.msg("Or, use `spack compiler remove -a` to remove all of them.")
        sys.exit(1)

    for compiler in compilers:
        spack.compilers.remove_compiler_from_config(
            compiler.spec, scope=args.scope)
        tty.msg("Removed compiler %s" % compiler.spec)


def compiler_info(args):
    """Print info about all compilers matching a spec."""
    cspec = spack.spec.CompilerSpec(args.compiler_spec)
    compilers = spack.compilers.compilers_for_spec(cspec, scope=args.scope)

    if not compilers:
        tty.die("No compilers match spec %s" % cspec)
    else:
        for c in compilers:
            print(str(c.spec) + ":")
            print("\tpaths:")
            for cpath in ['cc', 'cxx', 'f77', 'fc']:
                print("\t\t%s = %s" % (cpath, getattr(c, cpath, None)))
            if c.flags:
                print("\tflags:")
                for flag, flag_value in iteritems(c.flags):
                    print("\t\t%s = %s" % (flag, flag_value))
            if len(c.environment) != 0:
                if len(c.environment.get('set', {})) != 0:
                    print("\tenvironment:")
                    print("\t    set:")
                    for key, value in iteritems(c.environment['set']):
                        print("\t        %s = %s" % (key, value))
            if c.extra_rpaths:
                print("\tExtra rpaths:")
                for extra_rpath in c.extra_rpaths:
                    print("\t\t%s" % extra_rpath)
            print("\tmodules  = %s" % c.modules)
            print("\toperating system  = %s" % c.operating_system)


def compiler_list(args):
    compilers = spack.compilers.all_compilers(scope=args.scope, init_config=False)

    # If there are no compilers in any scope, and we're outputting to a tty, give a
    # hint to the user.
    if len(compilers) == 0:
        if not sys.stdout.isatty():
            return
        msg = "No compilers available"
        if args.scope is None:
            msg += ". Run `spack compiler find` to autodetect compilers"
        tty.msg(msg)
        return

    index = index_by(compilers, lambda c: (c.spec.name, c.operating_system, c.target))

    tty.msg("Available compilers")

    # For a container, take each element which does not evaluate to false and
    # convert it to a string. For elements which evaluate to False (e.g. None)
    # convert them to '' (in which case it still evaluates to False but is a
    # string type). Tuples produced by this are guaranteed to be comparable in
    # Python 3
    convert_str = (
        lambda tuple_container:
        tuple(str(x) if x else '' for x in tuple_container))

    index_str_keys = list(
        (convert_str(x), y) for x, y in index.items())
    ordered_sections = sorted(index_str_keys, key=lambda item: item[0])
    for i, (key, compilers) in enumerate(ordered_sections):
        if i >= 1:
            print()
        name, os, target = key
        os_str = os
        if target:
            os_str += "-%s" % target
        cname = "%s{%s} %s" % (spack.spec.compiler_color, name, os_str)
        tty.hline(colorize(cname), char='-')
        colify(reversed(sorted(c.spec for c in compilers)))


def add_compilers(parser, args):
    action = {'add': compiler_find,
              'find': compiler_find,
              'remove': compiler_remove,
              'rm': compiler_remove,
              'info': compiler_info,
              'list': compiler_list}
    action[args.compiler_command](args)
