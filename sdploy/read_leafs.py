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

import os
import inspect
import llnl.util.tty as tty
from .stack_file import StackFile
from .util import *

class FilterException(Exception):
    """Exception raised when filter evaluation fails"""

    def __init__(self, filter, filter_value):
        self.filter = filter
        self.filter_value = filter_value

class ReadLeaf(StackFile):
    """Manage the packages section in stack.yaml"""

    def __init__(self, config):
        """Declare class structs"""

        # Configuration
        self.platform_file = config.platform_yaml
        self.stack_file = config.stack_yaml
        self.leafs = []

    def read_key(self, key):
        """Regroup compilers for parsing in specs"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        # Read stack file
        compilers = ReadYaml()
        tty.info(f'Reading stack from file {self.stack_file}')
        compilers.read(os.path.join(self.stack_file))

        # Get only PE section
        data = self.group_sections(compilers.data, 'pe')

        # Replace tokens found in platform file
        self.replace_tokens(data)

        # Gather compilers in leafs
        self._leafs_from_dict(data, key)

    def report_leafs(self):
        """Report one item per line with dash"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        tty.info(f'The following items were found in {self.stack_file}')
        for leaf in self.leafs:
            print(f'- {leaf}')

    def write_to_file(self, filename):
        """Report leafs in a row to filename (to feed spack install)"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        tty.info(f'Leafs written to {filename}')
        with open(filename, 'w') as f:
            f.write(' '.join(self.leafs))

    def _leafs_from_dict(self, dic, key):
        """Returns list of values whose key is a string named key"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        for k,v in dic.items():
            if isinstance(v, dict):
                self._leafs_from_dict(v, key)
            if isinstance(v, str):
                if k == key:
                    self.leafs.append(v)

