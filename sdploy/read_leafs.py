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

import os
from collections.abc import MutableMapping
from copy import deepcopy
import inspect

from pdb import set_trace as st
from .yaml_manager import ReadYaml

class FilterException(Exception):
    """Exception raised when filter evaluation fails"""
    def __init__(self, filter, filter_value):
        self.filter = filter
        self.filter_value = filter_value


class ReadLeaf(ReadYaml):
    """Manage the packages section in stack.yaml"""

    def __init__(self, platform_file, stack_file, debug):
        """Declare class structs"""

        # Configuration
        self.platform_file = platform_file
        self.stack_file = stack_file
        self.debug = debug
        self.leafs = []

    def read_key(self, key):
        """Regroup compilers for parsing in specs"""

        if self.debug:
            print(f'Entering function: {inspect.stack()[0][3]}')

        # Read stack file
        compilers = ReadYaml()
        tty.info(f'Reading stack from file {self.stack_file}')
        compilers.read(os.path.join(self.stack_file))

        # Get only PE section
        data = self.group_sections(compilers.data, 'pe')

        # Gather compilers in compilers list
        self._leafs_from_dict(data, key)

    def _leafs_from_dict(self, dic, key):
        """Returns list of values whose key is a string named key"""

        if self.debug:
            print(f'Entering function: {inspect.stack()[0][3]}')

        for k,v in dic.items():
            if isinstance(v, dict):
                self._leafs_from_dict(v, key)
            if isinstance(v, str):
                if k == key:
                    self.leafs.append(v)

