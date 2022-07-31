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

description = "write packages.yaml file"
section = "Sdploy"
level = "short"

from ..yaml_manager import ReadYaml
from ..packages import Packages
from ..util import *
from ..config import *

def setup_parser(subparser):
    subparser.add_argument(
        '-p', '--platform', required=True,
        help='path to the pplatform file.'
    )
    subparser.add_argument(
        '-o', '--output-path',
        help='where to write spack.yaml'
    )

    subparser.add_argument(
        '-i', '--input-path',
        help='where to find stack.yaml'
    )

    subparser.add_argument(
        '-tp', '--templates-path',
        help='where to find jinja templates'
    )

    subparser.add_argument(
        '-tf', '--template-file',
        help='where to find jinja templates'
    )

    subparser.add_argument(
        '-s', '--source-file',
        help='if file not named stack.yaml (not in use)'
    )

    subparser.add_argument(
        '-a', '--arch', help='CPU architecture (not in use)'
    )

    subparser.add_argument(
        '-g', '--gpu', help='GPU manufacture, if any (not in use)'
    )

    subparser.add_argument(
        '-n', '--network', help='type of network (not in use)'
    )

def write_packages_yaml(parser, args):
    """Create spack.yaml file"""

    # Read sdploy configuration.
    # Items read from configuration may apply if no option was given in the
    # command line. Note that there aren't options for every single item that
    # can be found in the configuration file.
    config = ReadYaml()
    config.read(get_prefix() + SEP + CONFIG_FILE)

    # Handle arguments.
    if not args.input_path:
        args.input_path = os.getcwd()
    if not args.output_path:
        args.output_path = os.getcwd()
    if not args.source_file:
        args.source_file = config.data['config']['stack_yaml']
    if not args.templates_path:
        args.templates_path = os.getcwd()
    if not args.template_file:
        args.template_file = config.data['config']['spack_yaml_template']

    stack_yaml = args.input_path + SEP + args.source_file
    spack_yaml = config.data['config']['spack_yaml']
    packages_yaml = config.data['config']['packages_yaml']
    packages_yaml_template = config.data['config']['packages_yaml_template']
    platform_yaml = args.platform

    # Initiates variables and does initial processing
    pkgs = Packages(platform_yaml, stack_yaml)

    # Create default packages dictionary
    pkgs.packages_yaml_packages()

    # Create external packages dictionary
    pkgs.packages_yaml_external()

    # Group dictionaries together. Further dictionaries can be added later
    # if new features are needed.
    data = {}
    data['defaults'] = pkgs.defaults
    data['externals'] = pkgs.external

    # Set up jinja
    file_loader = FileSystemLoader(args.templates_path)
    env = Environment(loader = file_loader, trim_blocks = True)

    # Render and write packages.yaml
    template = env.get_template(packages_yaml_template)
    output = template.render(packages = data)
    print(output)
    with open(packages_yaml, 'w') as f:
        f.write(output)

