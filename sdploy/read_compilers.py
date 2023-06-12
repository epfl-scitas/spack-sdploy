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
            if self._skip_list(stack):
                continue

            for stack_name, stack in stack.items():
                if stack_name in ['filters', 'metadata']:
                    continue
                # The order is important:
                # - compiler_spec has priority over compiler
                if 'compiler_spec' in stack:
                    compilers.append('{} %{}'.format(stack['compiler_spec'], core_compiler))
                elif 'compiler' in stack:
                    compilers.append('{} %{}'.format(stack['compiler'], core_compiler))
                else:
                    print(f'No compiler found for PE {pe} {stack_name}')

        return compilers
