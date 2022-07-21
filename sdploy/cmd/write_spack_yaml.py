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
section = "SCITAS"
level = "short"

from ..yaml_manager import ReadYaml
from ..pe import ProgrammingEnvironment
from ..packages import Packages

def setup_parser(subparser):
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

def write_spack_yaml(parser, args):
    """Create spack.yaml file"""

    # Process arguments.
    # The following definitions will later me moved to a separate file:
    # - stack.yaml
    # - spack.yaml.j2
    # - spack_yaml
    # As well as the schema keywords:
    # - pe
    # - packages
    if not args.input_path:
        args.input_path = os.getcwd()
    if not args.output_path:
        args.output_path = os.getcwd()
    if not args.source_file:
        args.source_file = 'stack.yaml'
    if not args.templates_path:
        args.templates_path = os.getcwd()
    if not args.template_file:
        args.template_file = 'spack.yaml.j2'

    stack_yaml = args.input_path + '/' + args.source_file
    spack_yaml = 'spack.yaml'
    packages_yaml = 'packages.yaml'
    packages_yaml_template = 'packages.yaml.j2'

    # Process Programming Environment section.
    pe = ProgrammingEnvironment(stack_yaml, stack_yaml)
    pe(section = 'pe')

    # Process Packages section.
    pkgs = Packages(stack_yaml, stack_yaml)
    pkgs(section = 'packages')

    # spack.yaml
    # Get all data in a single dictionary
    data = deepcopy(pe.flat_stack)
    data['packages'] = pkgs.pkg_defs
    data['pkgs_pe'] = pkgs.pe

    # All of this will go in to a class/method
    file_loader = FileSystemLoader(args.templates_path)
    env = Environment(loader = file_loader, trim_blocks = True)

    # Render and write spack.yaml
    template = env.get_template(args.template_file)
    output = template.render(stack = data)
    print(output)
    with open(spack_yaml, 'w') as f:
        f.write(output)

    template = env.get_template(packages_yaml_template)
    output = template.render(packages = pkgs.pkgs_yaml)
    print(output)
    with open(packages_yaml, 'w') as f:
        f.write(output)

#    test = ReadYaml()
#    test.read('test.yaml')
