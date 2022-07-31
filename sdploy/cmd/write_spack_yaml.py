##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import argparse
import collections
import sys
import os

import spack
import spack.cmd

from copy import deepcopy
from jinja2 import Environment, FileSystemLoader
from pdb import set_trace as st

description = "write spack.yaml file"
section = "Sdploy"
level = "short"

from ..yaml_manager import ReadYaml
from ..spack_yaml import SpackYaml
from ..util import *
from ..config import *

def setup_parser(subparser):
    subparser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='print debug information.'
    )
    subparser.add_argument(
        '-p', '--platform',
        help='path to the platform file.'
    )
    subparser.add_argument(
        '-s', '--stack',
        help='path to the stack file'
    )
    subparser.add_argument(
        '-tp', '--templates-path',
        help='where to find jinja templates'
    )
    subparser.add_argument(
        '-tf', '--template-file',
        help='where to find jinja templates'
    )

def write_spack_yaml(parser, args):
    """Create spack.yaml file"""

    # Read sdploy configuration.
    # Items read from configuration may apply if no option was given in the
    # command line. Note that there aren't options for every single item that
    # can be found in the configuration file.
    config = ReadYaml()
    config.read(get_prefix() + SEP + CONFIG_FILE)

    # Handle arguments.
    # sdploy will prefer command line over declared arguments in sdploy.yaml

    # General information about the hardware available
    # If defined anywhere, we will use the file provided in the platforms directory
    if not args.platform:
        if 'platform_yaml' in config.data['config']:
            if config.data['config']['platform_yaml'] is None:
                args.platform = os.getcwd() + SEP + 'platforms' + SEP + 'platform.yaml'
            else:
                args.platform = config.data['config']['platform_yaml']
    if not args.stack:
        if 'stack_yaml_path' in config.data['config']:
            if config.data['config']['stack_yaml_path'] is None:
                args.stack = os.getcwd() + SEP + 'samples/stack.yaml'
            else:
                args.stack = config.data['config']['stack_yaml_path']
    if not args.templates_path:
        args.templates_path = os.getcwd() + SEP + 'templates'
    if not args.template_file:
        args.template_file = config.data['config']['spack_yaml_template']

    debug = args.debug
    stack_yaml = args.stack
    platform_yaml = args.platform
    spack_yaml = config.data['config']['spack_yaml']

    # Process Programming Environment section.
    stack = SpackYaml(platform_yaml, stack_yaml, debug)

    # Create PE definitions dictionary
    stack.create_pe_definitions_dict()

    # Create packages definitions dictionary
    stack.create_pkgs_definitions_dict()

    # Create PE matrix dictionary
    stack.create_pe_compiler_specs_dict()

    # Create PE support libraries matrix dictionary
    stack.create_pe_libraries_specs_dict()

    # Create package lists matrix dictionary
    stack.create_pkgs_specs_dict()

    # Concatenate all dicts
    data = {}
    data['pe_defs'] = stack.pe_defs
    data['pkgs_defs'] = stack.pkgs_defs
    data['pe_specs'] = stack.pe_specs
    data['pkgs_specs'] = stack.pkgs_specs

    # Jinja setup
    file_loader = FileSystemLoader(args.templates_path)
    env = Environment(loader = file_loader, trim_blocks = True)

    # Render and write spack.yaml
    template = env.get_template(args.template_file)
    output = template.render(stack = data)
    print(output)
    with open(spack_yaml, 'w') as f:
        f.write(output)
