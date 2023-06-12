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

description = "write spack.yaml file"
section = "Sdploy"
level = "short"

from ..spack_yaml import SpackYaml
from ..util import st
from ..config import *
from ..config_manager import Config
from ..common_parser import setup_parser


def write_spack_yaml(parser, args):
    """Create spack.yaml file"""

    config = Config(args)

    # Process Programming Environment section.
    stack = SpackYaml(config)

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
    data['definitions_list'] = stack.definitions_list
    data['configs'] = config.configs
    data['pe_compilers'] = list(stack.pe_compilers.values())
    tty.debug(stack.definitions_list)

    stack.write_yaml(data = data)
