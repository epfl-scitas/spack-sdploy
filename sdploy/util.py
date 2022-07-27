import os
from .yaml_manager import ReadYaml

def get_prefix():
    """Return path to current module"""

    return(get_subdir(__loader__.get_filename(),2))

def get_subdir(path, level = 1, sep = '/'):
    """Return subdirectory of specified level

    /scratch/site/user/dev -> /scratch/site/user (level=1)
    /scratch/site/user/dev -> /scratch/site      (level=2)
    """

    path_list = path.split(sep)
    dir_levels = path_list[1:len(path_list) - level]
    return (sep + sep.join(dir_levels))
