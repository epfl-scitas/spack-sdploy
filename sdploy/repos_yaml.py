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
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, working_dir
from spack.util.executable import ProcessError, which

from .yaml_manager import ReadYaml
from .util import *

from pdb import set_trace as st

class FilterException(Exception):
    """Exception raised when filter evaluation fails"""
    def __init__(self, filter, filter_value):
        self.filter = filter
        self.filter_value = filter_value


class ReposYaml(ReadYaml):
    """Manage the packages section in stack.yaml"""

    def __init__(self, stack, debug=False):
        """Declare class structs"""

        # Configuration files
        self.stack_file = os.path.join(get_prefix(), 'stacks', stack, stack + '.yaml')
        self.commons_file = os.path.join(get_prefix(), 'stacks', stack, 'common.yaml')
        self.debug = debug

        # Load files into dicts
        self._load_data()

    def _load_data(self):
        """Read configuration"""

        self.stack = self.get_data(self.stack_file)
        self.commons = self.get_data(self.commons_file)

    def clone(self):
        """Read repositories declared in commons.yaml to be cloned and call clone method"""

        for repo in self.commons['extra_repos'].keys():
            repo_url = self.commons['extra_repos'][repo]['repo']
            repo_path = self.commons['extra_repos'][repo]['path']
            repo_tag = self.commons['extra_repos'][repo]['tag']
            prefix = os.path.join(self.commons['work_directory'],
                                  self.commons['stack_release'],
                                  self.commons['spack_external'])
            self._clone(repo_url, repo_path, repo_tag, os.path.join(prefix,repo_path))

    def _clone(self, url, path, tag, prefix):
        """Clone repository"""

        origin_url = url
        branch = tag
        #origin_url, branch = get_origin_info(args.remote)
        #prefix = args.prefix
        # tty.msg("Fetching spack from '%s': %s" % (args.remote, origin_url))

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



