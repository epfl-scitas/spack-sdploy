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
from .yaml_manager import ReadYaml
from .util import *
from .config import *

class Config(object):
    """This class will handle the parsing of the arguments for all the commands.
    Its only goal is to define an argument and decide if its value should come
    from the:

            1.values defined in the command line (highest priority)
            2.values defined in sdploy.yaml
            3.hardcoded values defined in util.py (lowest priority)"""

    def __init__(self, args):
        """Only function in the class"""

        self.debug = False
        self.stacks = None
        self.stack_yaml = None
        self.platform_yaml = None
        self.templates_path = None
        self.spack_yaml_template = None
        self.spack_compilers_yaml_template = None
        self.packages_yaml_template = None
        self.modules_yaml_template = None
        self.spack_yaml = None
        self.spack_yaml_path = None
        self.packages_yaml = None
        self.packages_yaml_path = None
        self.modules_yaml = None
        self.modules_yaml_path = None

        # Read sdploy configuration.
        config = ReadYaml()
        config.read(get_prefix() + SEP + CONFIG_FILE)

        # spack-sdploy will check if an argument was given through the command
        # line. If an value was passed to the argument in the command line,
        # then this value will be stored. If no value was passed through the
        # command line, then spack-sdploy will see if there is a value defined
        # in the sdploy.yaml file. If a value exists for the argument in this
        # file then this is the value that will be stored. Finaly, if no value
        # was given through the command line, nor it is defined in sdploy.yaml
        # file, then spack-sdploy will be used the value defined by default in
        # the util module.

        if args.debug == True:
            self.debug = True

        # PATH/FILENAME: stack file, for example, '/path/to/stack.yaml'
        if not args.stack:
            if 'stack_yaml' in config.data['config']:
                if config.data['config']['stack_yaml'] is None:
                    self.stack_yaml = stack_yaml
                else:
                    self.stack_yaml = config.data['config']['stack_yaml']
        else:
            self.stack_yaml = args.stack


        # PATH/FILENAME: platform file, for example, '/path/to/platform.yaml'
        if not args.platform:
            if 'platform_yaml' in config.data['config']:
                if config.data['config']['platform_yaml'] is None:
                    self.platform_yaml = platform_yaml
                else:
                    self.platform_yaml = config.data['config']['platform_yaml']
        else:
            self.platform_yaml = args.platform

        # PATH: jinja templates directory, for example, '/path/to/templates'
        if not args.templates_path:
            if 'templates_path' in config.data['config']:
                if config.data['config']['templates_path'] is None:
                    self.templates_path = templates_path
                else:
                    self.platform = config.data['config']['templates_path']
        else:
            self.templates_path = args.templates_path

        # FILENAME: template for spack.yaml, for example, 'spack.yaml.j2'
        if 'spack_yaml_template' in config.data['config']:
                if config.data['config']['spack_yaml_template'] is not None:
                    self.spack_yaml_template = config.data['config']['spack_yaml_template']

        # FILENAME: template for spack-compilers.yaml, for example, 'spack-compilers.yaml.j2'
        if 'spack_compilers_yaml_template' in config.data['config']:
                if config.data['config']['spack_compilers_yaml_template'] is not None:
                    self.spack_compilers_yaml_template = config.data['config']['spack_compilers_yaml_template']

        # FILENAME: template for packages.yaml, for example, 'packages.yaml.j2'
        if 'packages_yaml_template' in config.data['config']:
                if config.data['config']['packages_yaml_template'] is not None:
                    self.packages_yaml_template = config.data['config']['packages_yaml_template']

        # FILENAME: template for modules.yaml, for example, 'modules.yaml.j2'
        if 'modules_yaml_template' in config.data['config']:
                if config.data['config']['modules_yaml_template'] is not None:
                    self.modules_yaml_template = config.data['config']['modules_yaml_template']

        # FILENAME: spack.yaml, for example, 'spack.yaml'
        if 'spack_yaml' in config.data['config']:
                if config.data['config']['spack_yaml'] is not None:
                    self.spack_yaml = config.data['config']['spack_yaml']

        # PATH: spack.yaml path, for example, '/path/to/config'
        #       -> does not include the file name
        if 'spack_yaml_path' in config.data['config']:
                if config.data['config']['spack_yaml_path'] is not None:
                    self.spack_yaml_path = config.data['config']['spack_yaml_path']

        # FILENAME: packages.yaml, for example, 'packages.yaml'
        if 'packages_yaml' in config.data['config']:
                if config.data['config']['packages_yaml'] is not None:
                    self.packages_yaml = config.data['config']['packages_yaml']

        # PATH: path to packages.yaml, for example, '/path/to/config'
        #       -> does not include the file name
        if 'packages_yaml_path' in config.data['config']:
                if config.data['config']['packages_yaml_path'] is not None:
                    self.packages_yaml_path = config.data['config']['packages_yaml_path']

        # FILENAME: modules.yaml, for example, 'modules.yaml'
        if 'modules_yaml' in config.data['config']:
                if config.data['config']['modules_yaml'] is not None:
                    self.modules_yaml = config.data['config']['modules_yaml']

        # PATH: path to modules.yaml, for example, '/path/to/config'
        #       -> does not include the file name
        if 'modules_yaml_path' in config.data['config']:
                if config.data['config']['modules_yaml_path'] is not None:
                    self.modules_yaml_path = config.data['config']['modules_yaml_path']

    def info(self):
        """Print debug information"""

        print(f'debug: {self.debug}')
        print(f'stack_yaml: {self.stack_yaml}')
        print(f'platform_yaml: {self.platform_yaml}')
        print(f'templates_path: {self.templates_path}')
        print(f'spack_yaml_template : {self.spack_yaml_template}')
        print(f'packages_yaml_template: {self.packages_yaml_template}')
        print(f'modules_yaml_template: {self.modules_yaml_template}')
        print(f'spack_yaml: {self.spack_yaml}')
        print(f'spack_yaml_path: {self.spack_yaml_path}')
        print(f'packages_yaml: {self.packages_yaml}')
        print(f'packages_yaml_path: {self.packages_yaml_path}')
        print(f'modules_yaml: {self.modules_yaml}')
        print(f'modules_yaml_path: {self.modules_yaml_path}')
