# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                       #
# SCITAS STACK DEPLOYMENT 2022, EPFL                                    #
#                                                                       #
# This module provides default values for all the variables. This       #
# enable spack-sdploy to work out-of-the-box.                           #
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
import sys
from .yaml_manager import ReadYaml
from .config import * # check if this is really necessary

import spack
import spack.cmd
import spack.config
import spack.environment as ev
from spack.util.executable import which

# The following line makes de tracer available
# every time this module is imported.
from pdb import set_trace as st

def get_prefix():
    """Return prefix of spack-sdploy"""

    return(get_subdir(__loader__.get_filename(), 2))

def get_subdir(path, level = 1, sep = None):
    """Return subdirectory of specified level

    /scratch/site/user/dev -> /scratch/site/user (level=1)
    /scratch/site/user/dev -> /scratch/site      (level=2)
    """

    sep = os.sep
    path_list = path.split(sep)
    dir_levels = path_list[1:len(path_list) - level]
    return (sep + sep.join(dir_levels))

# If the user does not specify any arguments after the command, we believe
# he is just trying some commands out-of-the-box and we use the samples directory.
# THIS DOES NOT WORK BECAUSE OF `-d` for debug
if len(sys.argv) <= 2:
    stack_dir = 'samples'
else:
    stack_dir = 'stacks'


#print("UTIL.PY")
#st()


# We don't give a default for the stack name. Whether the user passes the name
# of the stack as an argument or we use the samples directory, in which case
# the name of the stack is known (stack).

# Set reasonable default values for first run. This values can be changed
# through the sdploy.yaml file or direcly from the command line.
stack = 'laptop'
stack_ver = 'v1'
prefix = os.path.join(get_prefix(), stack_dir)
stack_yaml = os.path.join(prefix, 'stack', 'stack.yaml')
platforms_dir = 'platforms'
platform = 'platform'
platform_yaml = os.path.join(prefix, 'stack', 'platforms', 'platform.yaml')
templates_dir = 'templates'
templates_path = os.path.join(prefix, 'stack', templates_dir)
# The following are the name of the template files
spack_yaml_template = 'spack.yaml.j2'
packages_yaml_template = 'packages.yaml.j2'
modules_yaml_template = 'modules.yaml.j2'
repos_yaml_template = 'repos.yaml.j2'
mirrors_yaml_template = 'mirrors.yaml.j2'
# Where to write files to
spack_install_path = ''
spack_config_path = get_prefix()
spack_yaml = 'spack.yaml'
spack_yaml_path = os.path.join(get_prefix(), 'output')
packages_yaml = 'packages.yaml'
packages_yaml_path = os.path.join(get_prefix(), 'output')
modules_yaml = 'modules.yaml'
modules_yaml_path = os.path.join(get_prefix(), 'output')
repos_yaml = 'repos.yaml'
repos_yaml_path = os.path.join(get_prefix(), 'output')
mirrors_yaml = 'mirrors.yaml'
mirrors_yaml_path = os.path.join(get_prefix(), 'output')

