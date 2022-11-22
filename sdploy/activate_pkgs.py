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

class ActivatePkgs(StackFile):
    """Manage the packages whose activation is necessary"""

    def __init__(self, config):
        """Declare class structs"""

        super().__init__(config)
        self.pkglist = []
        self._add_activated_lists()
        self._add_activated_pkgs()
        self.pkglist = set(self.pkglist)

    def _add_activated_lists(self):
        """Add packages from lists having 'activate: true' attribute"""

        for _, v in self.data.items():
            # if activated in metadata then it is a packages list
            if 'activated' in v['metadata']:
                for pkg in v['packages']:
                    if isinstance(pkg, str):
                        self.pkglist.append(pkg)
                    elif isinstance(pkg, dict):
                        self.pkglist.append(list(pkg.keys()).pop())

    def _add_activated_pkgs(self):
        """Add packages from lists NOT having 'activate: true' attribute.
        This packages are activated using its own attribute."""

        for _, v in self.data.items():
            if v['metadata']['section'] == 'packages':
                for pkg in v['packages']:
                    if isinstance(pkg, dict):
                        for pkg_name, prop in pkg.items():
                            if 'activated' in prop:
                                self.pkglist.append(pkg_name)

    def write_activated_pkgs(self):
        """Write activated packages to file, one per line"""

        with open('packages_to_activate', 'w') as f:
            for p in self.pkglist:
                f.write(p + '\n')
