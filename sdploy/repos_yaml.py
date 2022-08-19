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
from pdb import set_trace as st

from .yaml_manager import ReadYaml
from .util import *

class ReposYaml(ReadYaml):
    """Manage the packages section in stack.yaml"""

    def __init__(self, config, debug=False):
        """Declare class structs"""

        # Configuration files
        self.config = config
        self.stack_file = os.path.join(config.stack_yaml)
        self.commons_file = os.path.join(config.commons_yaml)
        self.debug = debug
        # Placement for repos dictionary needed for repos.yaml
        self.repos = {}
        # Load files contents into dictionaries
        self._load_data()

    def _write_yaml(self, output, filename):

        with fs.write_tmp_and_move(os.path.realpath(filename)) as f:
            yaml = syaml.load_config(output)
            # spack.config.validate(yaml, spack.schema.env.schema, filename)
            syaml.dump_config(yaml, f, default_flow_style=False)

    def write_yaml(self):
        """Write repos.yaml"""

        # Jinja setup
        file_loader = FileSystemLoader(self.config.templates_path)
        jinja_env = Environment(loader = file_loader, trim_blocks = True)

        # Check that template file exists
        path = os.path.join(self.config.templates_path, self.config.repos_yaml_template)
        if not os.path.exists(path):
            tty.die(f'Template file {self.config.repos_yaml_template} does not exist ',
                    f'in {path}')

        # Render and write repos.yaml
        template = jinja_env.get_template(self.config.repos_yaml_template)
        output = template.render(repos = self.repos)

        tty.msg(self.config.repos_yaml)
        print(output)

        env = ev.active_environment()
        if env:
            self._write_yaml(output, os.path.realpath(env.manifest_path))
        else:
            filename = os.path.join(self.config.spack_config_path, self.config.repos_yaml)
            tty.msg(f'Writing file {filename}')
            self._write_yaml(output, filename)

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

            # self.repos will be needed later for creating repos.yaml
            self.repos[repo_path] = os.path.join(prefix,repo_path)
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



