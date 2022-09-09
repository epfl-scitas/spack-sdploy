import llnl.util.tty as tty

description = "list-mirrors"
section = "Sdploy"
level = "short"

from ..mirrors_yaml import MirrorsYaml
from ..config_manager import Config
from ..common_parser import setup_parser

def list_mirrors(parser, args):
    """Returns list of comilers defined in stack"""

    config = Config(args)

    # Instantiate ModulesYaml class
    mirrors = MirrorsYaml(config)

    print('\n'.join(['{}: {}'.format(k, v) for k, v in mirrors.mirrors['paths'].items()]))
