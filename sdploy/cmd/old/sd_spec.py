# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import sys

import llnl.util.lang as lang
import llnl.util.tty as tty

import spack
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.hash_types as ht
import spack.spec
import spack.store

description = "show what would be installed, given a spec"
section = "Sdploy"
level = "short"

from ..util import *
from ..config import *
from ..spack_yaml import SpackYaml
from ..config_manager import Config

def setup_parser(subparser):

    #                                                                               
    # spack-sdploy specific options
    #                                                                               

    subparser.add_argument(
        '-s', '--stack',
        help='path to the stack file'
    )
#    subparser.add_argument(
#        '-p', '--platform',
#        help='path to the platform file.'
#    )
#    subparser.add_argument(
#        '--prefix',
#        help='path to the stacks directory.'
#    )
#    subparser.add_argument(
#        '-d', '--debug', action='store_true', default=False,
#        help='print debug information.'
#    )

    subparser.epilog = """\
when an environment is active and no specs are provided, the environment root \
specs are used instead

for further documentation regarding the spec syntax, see:
    spack help --spec
"""
    arguments.add_common_arguments(
        subparser, ['long', 'very_long', 'install_status', 'stack']
    )
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument(
        '-y', '--yaml', action='store_const', dest='format', default=None,
        const='yaml', help='print concrete spec as YAML')
    format_group.add_argument(
        '-j', '--json', action='store_const', dest='format', default=None,
        const='json', help='print concrete spec as JSON')
    format_group.add_argument(
        '--format', action='store', default=None,
        help='print concrete spec with the specified format string')
    subparser.add_argument(
        '-c', '--cover', action='store',
        default='nodes', choices=['nodes', 'edges', 'paths'],
        help='how extensively to traverse the DAG (default: nodes)')
    subparser.add_argument(
        '-N', '--namespaces', action='store_true', default=False,
        help='show fully qualified package names')
    subparser.add_argument(
        '-t', '--types', action='store_true', default=False,
        help='show dependency types')
#    subparser.add_argument(
#        '-s', '--stack',
#        help='path to the stack file'
#    )
    subparser.add_argument(
        '-p', '--platform',
        help='path to the platform file.'
    )
    subparser.add_argument(
        '--prefix',
        help='path to the stacks directory.'
    )
    subparser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='print debug information.'
    )

    arguments.add_common_arguments(subparser, ['specs'])

    spack.cmd.common.arguments.add_concretizer_args(subparser)


def sd_spec(parser, args):

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # spack-sdploy: start
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    st()
    config = Config(args)
    if config.debug:
        config.info()

    # Process Programming Environment section.
    stack = SpackYaml(config.platform_yaml, config.stack_yaml, config.debug)

    # Create PE definitions dictionary
    stack.create_pe_definitions_dict(core = False)

    compilers = []
    for pkg in stack.pe_defs:
        if pkg.endswith('compiler'):
            compilers.append(stack.pe_defs[pkg])

    tty.msg(f'Found the following specs:')
    for compiler in compilers:
        print(f'    - {compiler}')

    args.specs = compilers

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # spack-sdploy: end
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    name_fmt = '{namespace}.{name}' if args.namespaces else '{name}'
    fmt = '{@version}{%compiler}{compiler_flags}{variants}{arch=architecture}'
    install_status_fn = spack.spec.Spec.install_status
    tree_kwargs = {
        'cover': args.cover,
        'format': name_fmt + fmt,
        'hashlen': None if args.very_long else 7,
        'show_types': args.types,
        'status_fn': install_status_fn if args.install_status else None
    }

    # use a read transaction if we are getting install status for every
    # spec in the DAG.  This avoids repeatedly querying the DB.
    tree_context = lang.nullcontext
    if args.install_status:
        tree_context = spack.store.db.read_transaction

    # Use command line specified specs, otherwise try to use environment specs.
    if args.specs:
        input_specs = spack.cmd.parse_specs(args.specs)
        specs = [(s, s.concretized()) for s in input_specs]
    else:
        env = ev.active_environment()
        if env:
            env.concretize()
            specs = env.concretized_specs()
        else:
            tty.die("spack spec requires at least one spec or an active environment")

    for (input, output) in specs:
        # With -y, just print YAML to output.
        if args.format:
            if args.format == 'yaml':
                # use write because to_yaml already has a newline.
                sys.stdout.write(output.to_yaml(hash=ht.dag_hash))
            elif args.format == 'json':
                print(output.to_json(hash=ht.dag_hash))
            else:
                print(output.format(args.format))
            continue

        with tree_context():
            # Only show the headers for input specs that are not concrete to avoid
            # repeated output. This happens because parse_specs outputs concrete
            # specs for `/hash` inputs.
            if not input.concrete:
                tree_kwargs['hashes'] = False  # Always False for input spec
                print("Input spec")
                print("--------------------------------")
                print(input.tree(**tree_kwargs))
                print("Concretized")
                print("--------------------------------")

            tree_kwargs['hashes'] = args.long or args.very_long
            print(output.tree(**tree_kwargs))