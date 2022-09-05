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
import shutil
import inspect

import spack
import spack.cmd
import spack.config
import spack.environment as ev
import spack.schema.env
import spack.util.spack_yaml as syaml
import llnl.util.filesystem as fs
import llnl.util.tty as tty

from llnl.util.filesystem import mkdirp, working_dir
from spack.util.executable import ProcessError, which

from jinja2 import Environment, FileSystemLoader

from .stack_file import StackFile
from .util import *

class ReposYaml(StackFile):
    """Manage the packages section in stack.yaml"""

    def __init__(self, config):
        """Declare class structs"""

        super().__init__(config)

        # These variables will be used in StackFile class.
        # Each command that write an Yaml file must define these 4 variables.
        # This technique allows for individual command customization of each
        # one of these parameters and at the same time the reuse of the functions
        # all gathered in a single module.
        self.templates_path = self.config.templates_path
        self.template_file = self.config.repos_yaml_template
        self.yaml_path = self.config.spack_config_path
        self.yaml_file = self.config.repos_yaml

        self.repos = {}
        self._load_data()
        #self._overload()

    def _overload(self):
        """Sets path to etc/spack if running outside environment"""

        self.yaml_path = os.path.join(
            self.commons['work_directory'],
            self.commons['stack_release'],
            self.commons['spack'] + '.' + self.commons['stack_version'],
            'etc/spack')

    def _load_data(self):
        """Read configuration"""

        self.stack = self.get_data(self.config.stack_yaml)
        self.commons = self.get_data(self.config.commons_yaml)

        for repo in self.commons['extra_repos'].keys():
            repo_url = self.commons['extra_repos'][repo]['repo']
            repo_path = self.commons['extra_repos'][repo]['path']
            repo_tag = self.commons['extra_repos'][repo]['tag']
            prefix = os.path.join(self.commons['work_directory'],
                                  self.commons['stack_release'],
                                  self.commons['spack_external'])

            self.repos[repo] = {
                'path': os.path.join(prefix, repo_path),
                'url': repo_url,
                'tag': repo_tag
            }
        
    def clone(self):
        """Read repositories declared in commons.yaml to be cloned and call clone method"""
        for repo, info in self.repos.items(): 
            self._clone(repo, **info)

    def _clone(self, repo, url=None, path=None, tag=None):
        """Clone repository"""

        git = which('git', required=True)
        if os.path.exists(path):
            tty.debug("Update repository {} in {}".format(repo, path))
            with working_dir(path):
                git('fetch', 'origin')
                git('checkout', tag)
        else:
            tty.debug("Clonining {}[{}] repository in {}".format(repo, url, path))
            git('clone', '-b', tag, url, path)





