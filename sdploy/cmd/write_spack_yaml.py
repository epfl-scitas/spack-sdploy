# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                       #
# SCITAS STACK DEPLOYMENT 2022, EPFL                                    #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

def write_spack_yaml(parser, args):
    """Create spack.yaml file"""

    config = Config(args)
    if config.debug:
        config.info()

    # Process Programming Environment section.
    stack = SpackYaml(config.platform_yaml, config.stack_yaml, config.debug)

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
    file_loader = FileSystemLoader(config.templates_path)
    env = Environment(loader = file_loader, trim_blocks = True)

    # Render and write spack.yaml
    template = env.get_template(config.spack_yaml_template)
    output = template.render(stack = data)
    print(output)
    with open(spack_yaml, 'w') as f:
        f.write(output)
