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
import os

from .yaml_manager import ReadYaml
from .util import *
from .config import *

class Config(object):
    """This class will handle the parsing of the arguments for all the commands.
    Its only goal is to define an argument and decide if its value should come
    from the:

            1.values defined in the command line (highest priority)
            2.values defined in sdploy.yaml
            3.hardcoded values defined in util.py (lowest priority)

    Note that not all values can be defined at the command line. In this case,
    the goal of this module is just to check if there is a values defined in
    sdploy.yaml a read in instead of the one defined in util.py"""

    def __init__(self, args):
        """Only function in the class"""

        self.debug = False
        self.prefix = None
        self.stack = None
        self.stack_path = None
        self.stack_yaml = None
        self.platform = None
        self.plarform_dir = None
        self.platforms_path = None
        self.platform_yaml = None
        self.commons_dir = None
        self.commons_path = None
        self.commons_yaml = None
        self.templates_dir = None
        self.templates_path = None
        self.spack_yaml_template = None
        self.spack_compilers_yaml_template = None
        self.packages_yaml_template = None
        self.modules_yaml_template = None
        self.repos_yaml_template = None
        self.mirrors_yaml_template = None
        self.spack_yaml = None
        self.spack_yaml_path = None
        self.packages_yaml = None
        self.packages_yaml_path = None
        self.modules_yaml = None
        self.modules_yaml_path = None

        # Read sdploy configuration.
        config = ReadYaml()
        config.read(os.path.join(get_prefix(), CONFIG_FILE))

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

        # prefix:
        # - it includes the 'samples' or 'stacks' subdir defined in util.py;
        if not args.prefix:
            if 'prefix' in config.data['config']:
                if config.data['config']['prefix'] is None:
                    self.prefix = prefix # from util.py
                else:
                    self.prefix = config.data['config']['prefix'] # from sdploy.yaml
        else:
            self.prefix = args.prefix # from arguments

        # stack:
        # - name of the stack, which is also a subdirectory under prefix;
        # - it is also the name of the stack yaml;
        if not args.stack:
            if 'stack' in config.data['config']:
                if config.data['config']['stack'] is None:
                    self.stack = stack # from util.py
                else:
                    self.stack = config.data['config']['stack'] # from sdploy.yaml
        else:
            self.stack = args.stack # from arguments

        # Once we know the name of the stack we can configure the fully qualified
        # name of the stack yaml file as well as the commons yaml file
        self.stack_path = os.path.join(self.prefix, self.stack)
        self.stack_yaml = os.path.join(self.stack_path, self.stack + '.yaml')
        self.commons_path = os.path.join(self.stack_path)
        self.commons_yaml = os.path.join(self.stack_path,
                                         config.data['config']['commons_yaml'])

        # platforms_dir:
        # - name of the platforms subdirectory under the stack
        if 'platforms_dir' in config.data['config']:
            if config.data['config']['platforms_dir'] is None:
                self.platforms_dir = config.data['config']['platforms_dir']
            else:
                self.platforms_dir = platforms_dir

        # Once we know the name of the platforms subdirectory, we can now configure
        # the fully qualifies path to this directory.
        self.platforms_path = os.path.join(self.prefix, self.stack, self.platforms_dir)

        # platform:
        # - name of the platform (environment)
        if not args.platform:
            if 'platform' in config.data['config']:
                if config.data['config']['platform'] is None:
                    self.platform = platform
                else:
                    self.platform = config.data['config']['platform']
        else:
            self.platform = args.platform

        # Once we know the name of the platform, we can compute the fully qualified
        # plaform yaml file name
        self.platform_yaml = os.path.join(self.platforms_path, self.platform + '.yaml')

        # templated_dir:
        # - name of the templates subdirectory under the stack
        if 'templates_dir' in config.data['config']:
            if config.data['config']['templates_dir'] is None:
                self.templates_dir = config.data['config']['templates_dir']
            else:
                self.templates_dir = templates_dir

        # Once we know the prefix, the stack name and the templates subdir name
        # we can configure its fully qualified path:
        self.templates_path = os.path.join(self.prefix, self.stack, self.templates_dir)

        # FILENAME: template for spack.yaml, for example, 'spack.yaml.j2'
        if 'spack_yaml_template' in config.data['config']:
            if config.data['config']['spack_yaml_template'] is not None:
                self.spack_yaml_template = config.data['config']['spack_yaml_template']
            else:
                self.spack_yaml_template = spack_yaml_template

        # FILENAME: template for packages.yaml, for example, 'packages.yaml.j2'
        if 'packages_yaml_template' in config.data['config']:
            if config.data['config']['packages_yaml_template'] is not None:
                self.packages_yaml_template = config.data['config']['packages_yaml_template']
            else:
                self.packages_yaml_template = packages_yaml_template

        # FILENAME: template for modules.yaml, for example, 'modules.yaml.j2'
        if 'modules_yaml_template' in config.data['config']:
            if config.data['config']['modules_yaml_template'] is not None:
                self.modules_yaml_template = config.data['config']['modules_yaml_template']
            else:
                self.modules_yaml_template = modules_yaml_template

        # FILENAME: template for repos.yaml, for example, 'repos.yaml.j2'
        if 'repos_yaml_template' in config.data['config']:
            if config.data['config']['repos_yaml_template'] is not None:
                self.repos_yaml_template = config.data['config']['repos_yaml_template']
            else:
                self.repos_yaml_template = repos_yaml_template

        # FILENAME: template for mirrors.yaml, for example, 'mirrors.yaml.j2'
        if 'mirrors_yaml_template' in config.data['config']:
            if config.data['config']['mirrors_yaml_template'] is not None:
                self.mirrors_yaml_template = config.data['config']['mirrors_yaml_template']
            else:
                self.mirrors_yaml_template = mirrors_yaml_template

        # FILENAME: spack.yaml, for example, 'spack.yaml'
        if 'spack_yaml' in config.data['config']:
            if config.data['config']['spack_yaml'] is not None:
                self.spack_yaml = config.data['config']['spack_yaml']
            else:
                self.spack_yaml = spack_yaml

        # PATH: spack.yaml path, for example, '/path/to/config'
        #       -> does not include the file name
        if 'spack_yaml_path' in config.data['config']:
            if config.data['config']['spack_yaml_path'] is not None:
                self.spack_yaml_path = config.data['config']['spack_yaml_path']
            else:
                self.spack_yaml_path = spack_yaml_path

        # FILENAME: packages.yaml, for example, 'packages.yaml'
        if 'packages_yaml' in config.data['config']:
            if config.data['config']['packages_yaml'] is not None:
                self.packages_yaml = config.data['config']['packages_yaml']
            else:
                self.packages_yaml = packages_yaml

        # PATH: path to packages.yaml, for example, '/path/to/config'
        #       -> does not include the file name
        if 'packages_yaml_path' in config.data['config']:
            if config.data['config']['packages_yaml_path'] is not None:
                self.packages_yaml_path = config.data['config']['packages_yaml_path']
            else:
                self.packages_yaml_path = packages_yaml_path

        # FILENAME: modules.yaml, for example, 'modules.yaml'
        if 'modules_yaml' in config.data['config']:
            if config.data['config']['modules_yaml'] is not None:
                self.modules_yaml = config.data['config']['modules_yaml']
            else:
                self.modules_yaml = modules_yaml

        # PATH: path to modules.yaml, for example, '/path/to/config'
        #       -> does not include the file name
        if 'modules_yaml_path' in config.data['config']:
            if config.data['config']['modules_yaml_path'] is not None:
                self.modules_yaml_path = config.data['config']['modules_yaml_path']
            else:
                self.modules_yaml_path = modules_yaml_path

        # FILENAME: repos.yaml, for example, 'repos.yaml'
        if 'repos_yaml' in config.data['config']:
            if config.data['config']['repos_yaml'] is not None:
                self.repos_yaml = config.data['config']['repos_yaml']
            else:
                self.repos_yaml = repos_yaml

        # PATH: path to repos.yaml, for example, '/path/to/config'
        #       -> does not include the file name
        if 'repos_yaml_path' in config.data['config']:
            if config.data['config']['repos_yaml_path'] is not None:
                self.repos_yaml_path = config.data['config']['repos_yaml_path']
            else:
                self.repos_yaml_path = repos_yaml_path

        # FILENAME: mirrors.yaml, for example, 'mirrors.yaml'
        if 'mirrors_yaml' in config.data['config']:
            if config.data['config']['mirrors_yaml'] is not None:
                self.mirrors_yaml = config.data['config']['mirrors_yaml']
            else:
                self.mirrors_yaml = mirrors_yaml

        # PATH: path to mirrors.yaml, for example, '/path/to/config'
        #       -> does not include the file name
        if 'mirrors_yaml_path' in config.data['config']:
            if config.data['config']['mirrors_yaml_path'] is not None:
                self.mirrors_yaml_path = config.data['config']['mirrors_yaml_path']
            else:
                self.mirrors_yaml_path = mirrors_yaml_path


    def info(self):
        """Print debug information"""

        print(f'debug: {self.debug}')
        print(f'prefix: {self.prefix}')
        print(f'stack: {self.stack}')
        print(f'stack_path: {self.stack_path}')
        print(f'stack_yaml: {self.stack_yaml}')
        print(f'platform: {self.platform}')
        print(f'platforms_dir: {self.platforms_dir}')
        print(f'platforms_path: {self.platforms_path}')
        print(f'platform_yaml: {self.platform_yaml}')
        print(f'commons_dir: {self.commons_dir}')
        print(f'commons_path: {self.commons_path}')
        print(f'commons.yaml: {self.commons_yaml}')
        print(f'templates_dir: {self.templates_dir}')
        print(f'templates_path: {self.templates_path}')
        print(f'spack_yaml_template : {self.spack_yaml_template}')
        print(f'packages_yaml_template: {self.packages_yaml_template}')
        print(f'modules_yaml_template: {self.modules_yaml_template}')
        print(f'repos_yaml_template: {self.repos_yaml_template}')
        print(f'mirrors_yaml_template: {self.mirrors_yaml_template}')
        print(f'spack_yaml: {self.spack_yaml}')
        print(f'spack_yaml_path: {self.spack_yaml_path}')
        print(f'packages_yaml: {self.packages_yaml}')
        print(f'packages_yaml_path: {self.packages_yaml_path}')
        print(f'modules_yaml: {self.modules_yaml}')
        print(f'modules_yaml_path: {self.modules_yaml_path}')
        print(f'repos_yaml: {self.repos_yaml}')
        print(f'repos_yaml_path: {self.repos_yaml_path}')
        print(f'mirrors_yaml: {self.mirrors_yaml}')
        print(f'mirrors_yaml_path: {self.mirrors_yaml_path}')
