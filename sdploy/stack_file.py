import llnl.util.tty as tty

from .yaml_manager import ReadYaml


class FilterException(Exception):
    """Exception raised when filter evaluation fails"""
    def __init__(self, filter, filter_value):
        self.filter = filter
        self.filter_value = filter_value


class StackFile(ReadYaml):
    """Common opertation for stack file managers"""

    def __init__(self, platform_file, stack_file):
        """Declare class structs"""

        # Configuration files
        self.platform_file = platform_file
        self.stack_file = stack_file

        # Original data
        self.data = {} # The original data

        # Tokens are set in yaml_manager
        self.filters = {}

        # Read stack.yaml into self.data attribute
        self.read(self.stack_file)

        # Replace tokens
        self.replace_tokens(self.data)

        # Read filters
        self.filters = self.read_filters(self.platform_file)


    def _remove_newline(self, values):
        return ' '.join((values.strip().split('\n')))

    def _handle_filter(self, attributes):
        result = []
        if isinstance(attributes, dict):
            # Check for filters presence
            for filter in self.filters.keys():
                if filter in attributes:
                    if self.filters[filter] in attributes[filter]:
                        values = attributes[filter][self.filters[filter]]
                        if isinstance(values, list):
                            result.extend(values)
                        else:
                            result.append(values)
                    else:
                        raise FilterException(filter, self.filters[filter])
        else: # We are just checking that attributes is not a structure (dict, list, etc)
            # We need to cast version to str because of ' '.join in next step
            result.append(str(attributes))
        return result
