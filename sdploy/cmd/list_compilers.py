# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
# SCITAS STACK DEPLOYMENT 2022, EPFL                                          #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import llnl.util.tty as tty

description = "list-compilers"
section = "Sdploy"
level = "short"

from ..read_compilers import Compilers
from ..config_manager import Config
from ..common_parser import setup_parser

from pdb import set_trace as st

def list_compilers(parser, args):
    """Returns list of comilers defined in stack"""

    config = Config(args)

    # Instantiate class
    compilers = Compilers(config)

    print('\n'.join(compilers.list_compilers()))
