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

description = "write packages.yaml file"
section = "Sdploy"
level = "short"

from ..yaml_manager import ReadYaml
from ..packages_yaml import PackagesYaml
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

