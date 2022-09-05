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
from copy import deepcopy
import llnl.util.tty as tty
from .stack_file import StackFile


class Compilers(StackFile):
    """Manage the packages section in stack.yaml"""

    def __init__(self, config):
        """Declare class structs"""
        super().__init__(config)
        
    def list_compilers(self):
        """Regroup compilers for parsing in specs"""

        core_compiler_data = self.group_sections(deepcopy(self.data), 'core')
        compilers_data = self.group_sections(deepcopy(self.data), 'pe')

        core_compiler = core_compiler_data['core']['compiler']

        compilers = []
        for pe, stack in compilers_data.items():
            for stack_name, stack in stack.items():
                if 'compiler' in stack:
                    compilers.append('{} %{}'.format(stack['compiler'], core_compiler))

        return compilers
