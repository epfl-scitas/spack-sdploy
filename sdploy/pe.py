from pdb import set_trace as st

from collections.abc import MutableMapping
from copy import deepcopy
from .yaml_manager import ReadYaml

class ProgrammingEnvironment(ReadYaml):
    """Manage the programming environment (PE) section in stack.yaml

    Provide usefull structures and methods that deal with the PE
    section of the stack.yaml file.

    self.stack -> stack whose entries are common (section parameter in __call__)
    self.flat_stack -> store a flattend dict whose keys are formed my the
                       composition of the nodes found in the tree from the
                       stack file.
    self.specs -> list containing all the specs found in the compilers section.
    """

    def __init__(self, platform_file, stack_file):
        """Declare class structs"""

        self.platform_file = platform_file
        self.stack_file = stack_file
        self.data = {} # used in ReadYaml but we highlight it here
        self.stack = {}
        self.flat_stack = {}
        self.specs = []
        self.filtered_stack = {}
        self._cursor = []

    def __call__(self, section):
        """Populate class structs"""

        # Reads stack.yaml into self.data
        self.read(self.stack_file)

        # Groups entries whose section = <section> in self.stack
        self.group_sections(deepcopy(self.data), section)

        # Execute replacements (common:variables)
        replace_tokens = self.read_replacements(self.platform_file)
        for key, value in replace_tokens.items():
            self.do_replace(self.stack, '<' + str(key) + '>', str(value))

        # Execute choices (common:filters)
        choose_tokens = self.read_choices(self.platform_file)
        for key, value in choose_tokens.items():
            self.do_choose(self.stack, self.stack, token={ key:value } )

        # Return a flat dictionary
        self.flat_stack = self.flatten_dict(self.stack)

        # Remove empty keys
        self.flat_stack = { key:self.flat_stack[key] for key in self.flat_stack
                           if self.flat_stack[key] is not None }
        self.flat_stack = { section : self.flat_stack }

    def flatten_dict(self, d: MutableMapping, parent_key: str = '', sep: str = '_'):
        """Returns a flat dict

        Return a 1-depth dict (flat) whose elements are formed by composing
        the nested dicts nodes using the separator sep.
        {'a':1, 'b':{'c':2}} -> {'a':1, 'b_c':2}
        origin: freecodecamp.org"""

        return dict(self._flatten_dict_gen(d, parent_key, sep))

    def group_sections(self, dic, section):
        """Return dictionary composed of common sections

        In the stack.yaml file there can be to different key that both are
        related to packages or to PE. This function will group all section
        which has section value in section key"""

        tmp = {}
        for key in dic:
            if dic[key]['metadata']['section'] == section:
                dic[key].pop('metadata')
                tmp[key] = dic[key]
        self.stack = tmp

    def _flatten_dict_gen(self, d, parent_key, sep):
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                yield from self.flatten_dict(v, new_key, sep=sep).items()
            else:
                yield new_key, v
