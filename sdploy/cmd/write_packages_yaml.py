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
from ..packages_yaml import Packages
from ..util import *
from ..config import *
from ..config_manager import Config

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
        '-t', '--templates-path',
        help='where to find jinja templates'
    )
    subparser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='print debug information.'
    )

def write_packages_yaml(parser, args):
    """Create spack.yaml file"""

    config = Config(args)
    if config.debug:
        config.info()

    # Initiates variables and does initial processing
    pkgs = Packages(config.platform_yaml, config.stack_yaml, config.debug)

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
    file_loader = FileSystemLoader(config.templates_path)
    env = Environment(loader = file_loader, trim_blocks = True)

    # Render and write packages.yaml
    template = env.get_template(config.packages_yaml_template)
    output = template.render(packages = data)
    print(output)
    with open(packages_yaml, 'w') as f:
        f.write(output)

