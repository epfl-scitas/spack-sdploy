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

def write_spack_yaml(parser, args):
    """Create spack.yaml file"""

    # Read sdploy configuration.
    # Items read from configuration may apply if no option was given in the
    # command line. Note that there aren't options for every single item that
    # can be found in the configuration file.
    config = ReadYaml()
    config.read(get_prefix() + SEP + CONFIG_FILE)

    # Handle arguments.
    # sdploy respect the following priority:
    #
    #  1.values defined in the command line (highest priority)
    #  2.values defined in sdploy.yaml
    #  3.hardcoded values defined in util.py (lowest priority)

    # FILENAME: stack file, for example, 'stack.yaml'
    if not args.stack:
        if 'stack_yaml_path' in config.data['config']:
            if config.data['config']['stack_yaml_path'] is None:
                args.stack = stack_yaml_path + SEP + stack_yaml
            else:
                args.stack = config.data['config']['stack_yaml_path']

    # FILENAME: platform file, for example, 'platform.yaml'
    if not args.platform:
        if 'platform_yaml' in config.data['config']:
            if config.data['config']['platform_yaml'] is None:
                args.platform = platform_yaml_path + SEP + platform_yaml
            else:
                args.platform = config.data['config']['platform_yaml']

    # PATH: jinja templates directory, for example, '/path/to/templates'
    if not args.templates_path:
        if 'templates_path' in config.data['config']:
            if config.data['config']['templates_path'] is None:
                args.templates_path = templates_path
            else:
                args.platform = config.data['config']['templates_path']

    # FILENAME: template for spack.yaml, for example, 'spack.yaml.j2'
    if 'spack_yaml_template' in config.data['config']:
            if config.data['config']['spack_yaml_template'] is not None:
                spack_yaml_template = config.data['config']['spack_yaml_template']

    # FILENAME: template for packages.yaml, for example, 'packages.yaml.j2'
    if 'packages_yaml_template' in config.data['config']:
            if config.data['config']['packages_yaml_template'] is not None:
                packages_yaml_template = config.data['config']['packages_yaml_template']

    # FILENAME: template for modules.yaml, for example, 'modules.yaml.j2'
    if 'modules_yaml_template' in config.data['config']:
            if config.data['config']['modules_yaml_template'] is not None:
                modules_yaml_template = config.data['config']['modules_yaml_template']

    # FILENAME: spack.yaml, for example, 'spack.yaml'
    if 'spack_yaml' in config.data['config']:
            if config.data['config']['spack_yaml'] is not None:
                spack_yaml = config.data['config']['spack_yaml']

    # PATH: spack.yaml path, for example, '/path/to/config'
    #       -> does not include the file name
    if 'spack_yaml_path' in config.data['config']:
            if config.data['config']['spack_yaml_path'] is not None:
                spack_yaml_path = config.data['config']['spack_yaml_path']

    # FILENAME: packages.yaml, for example, 'packages.yaml'
    if 'packages_yaml' in config.data['config']:
            if config.data['config']['packages_yaml'] is not None:
                packages_yaml = config.data['config']['packages_yaml']

    # PATH: path to packages.yaml, for example, '/path/to/config'
    #       -> does not include the file name
    if 'packages_yaml_path' in config.data['config']:
            if config.data['config']['packages_yaml_path'] is not None:
                packages_yaml_path = config.data['config']['packages_yaml_path']

    # FILENAME: modules.yaml, for example, 'modules.yaml'
    if 'modules_yaml' in config.data['config']:
            if config.data['config']['modules_yaml'] is not None:
                modules_yaml = config.data['config']['modules_yaml']

    # PATH: path to modules.yaml, for example, '/path/to/config'
    #       -> does not include the file name
    if 'modules_yaml_path' in config.data['config']:
            if config.data['config']['modules_yaml_path'] is not None:
                modules_yaml_path = config.data['config']['modules_yaml_path']

    debug = args.debug

    # Process Programming Environment section.
    stack = SpackYaml(platform_yaml_path + SEP + platform_yaml,
                      stack_yaml_path + SEP + stack_yaml, debug)

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
    template = env.get_template(spack_yaml_template)
    output = template.render(stack = data)
    print(output)
    with open(spack_yaml, 'w') as f:
        f.write(output)
