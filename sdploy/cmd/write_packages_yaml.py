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
import llnl.util.tty as tty

description = "write packages.yaml file"
section = "Sdploy"
level = "short"

from ..packages_yaml import PackagesYaml
from ..util import st
from ..config import *
from ..config_manager import Config
from ..common_parser import setup_parser

def write_packages_yaml(parser, args):
    """Create spack.yaml file"""

    config = Config(args)
    tty.debug(config.info())

    # Initiates variables and does initial processing
    pkgs = PackagesYaml(config)

    # Create default packages dictionary
    pkgs.packages_yaml_packages()

    # Create external packages dictionary
    pkgs.packages_yaml_external()

    # Create providers section dictionary
    pkgs.packages_yaml_providers()

    # Group dictionaries together. Further dictionaries can be added later
    # if new features are needed.
    data = {}
    data['defaults'] = pkgs.defaults
    data['externals'] = pkgs.externals
    data['providers'] = pkgs.providers

    pkgs.write_yaml(packages = data)
