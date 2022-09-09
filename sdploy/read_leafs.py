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

class ReadCompilers(StackFile):
    """Manage the packages section in stack.yaml"""

    def __init__(self, config):
        """Declare class structs"""

        # Configuration
        self.platform = config.platform
        self.platform_file = config.platform_yaml
        self.stack_file = config.stack_yaml
        self.leafs = []

    def list_compilers(self, key):
        """Regroup compilers for parsing in specs"""

        core_compiler_data = self.group_sections(deepcopy(self.data), 'core')
        compilers_data = self.group_sections(deepcopy(self.data), 'pe')

        core_compiler = core_compiler_data['compiler']
        
        self.replace_tokens(core_compiler_data)
        self.replace_tokens(compilers_data)

        compilers = []
        for pe, stack in compilers_data.items():
            for stack_name, stack in stack.items():
                if 'compiler' in stack:
                    compilers.append('{} %{}', compiler, core_compiler_data)

        return
