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
        self._overload()

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

    def clone(self):
        """Read repositories declared in commons.yaml to be cloned and call clone method"""

        for repo in self.commons['extra_repos'].keys():
            repo_url = self.commons['extra_repos'][repo]['repo']
            repo_path = self.commons['extra_repos'][repo]['path']
            repo_tag = self.commons['extra_repos'][repo]['tag']
            prefix = os.path.join(self.commons['work_directory'],
                                  self.commons['stack_release'],
                                  self.commons['spack_external'])

            # self.repos will be needed later for creating repos.yaml
            self.repos[repo_path] = os.path.join(prefix,repo_path)
            self._clone(repo_url, repo_path, repo_tag, os.path.join(prefix,repo_path))

    def _clone(self, url, path, tag, prefix):
        """Clone repository"""

        origin_url = url
        branch = tag

        if os.path.isfile(prefix):
            tty.die("There is already a file at %s" % prefix)

        if os.path.exists(os.path.join(prefix)):
            tty.warn("There already seems to be repository in %s" % prefix)
            tty.warn("Deleting the repository in %s" % prefix)
            try:
                shutil.rmtree(prefix)
            except:
                pass

        mkdirp(prefix)

        with working_dir(prefix):
            git = which('git', required=True)
            git('init', '--shared', '-q')
            git('remote', 'add', 'origin', origin_url)
            git('fetch', 'origin', '%s:refs/remotes/origin/%s' % (branch, branch),
                '-n', '-q')
            git('reset', '--hard', 'origin/%s' % branch, '-q')
            git('checkout', '-B', branch, 'origin/%s' % branch, '-q')

            tty.msg("Successfully created a new repository in %s" % prefix)



