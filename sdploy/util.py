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
from .yaml_manager import ReadYaml
from .config import *

# The following line makes de tracer available
# every time this module is imported.
from pdb import set_trace as st

def get_prefix():
    """Return prefix of spack-sdploy"""

    return(get_subdir(__loader__.get_filename(), 2))

def get_subdir(path, level = 1, sep = '/'):
    """Return subdirectory of specified level

    /scratch/site/user/dev -> /scratch/site/user (level=1)
    /scratch/site/user/dev -> /scratch/site      (level=2)
    """

    path_list = path.split(sep)
    dir_levels = path_list[1:len(path_list) - level]
    return (sep + sep.join(dir_levels))

# Set reasonable default values for first run. This values can be changed
# through the sdploy.yaml file or direcly from the command line.
stack_yaml = get_prefix() + SEP + 'samples' + SEP + 'stack.yaml'
platform_yaml = get_prefix() + SEP + 'platforms' + SEP + 'platform.yaml'
templates_path = get_prefix() + SEP + 'templates'
spack_yaml_template = 'spack.yaml.j2'
packages_yaml_template = 'packages.yaml.j2'
modules_yaml_template = 'modules.yaml.j2'
spack_yaml = 'spack.yaml'
spack_yaml_path = get_prefix() + SEP + 'output'
packages_yaml = 'packages.yaml'
packages_yaml_path = get_prefix() + SEP + 'output'
modules_yaml = 'modules.yaml'
modules_yaml_path = get_prefix() + SEP + 'output'
