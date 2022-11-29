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
        self._pe_definitions = self._define_PEs()
        self._add_activated_lists()
        self._add_activated_pkgs()
        self.pkglist = set(self.pkglist)

    def _get_pe_spec(self, definition):
        def_ = dict(definition)
        pe_name = def_['pe'][0]
        if pe_name not in self._pe_definitions:
            return ''

        pe = self._pe_definitions[pe_name]
        spec = f'''%{pe['compiler']} arch=linux-{self.tokens['os']}-{self.tokens['target']}'''
        if 'dependencies' in def_:
            for dep in def_['dependencies']:
                spec = f'''^{pe[dep]} {spec}'''
        return spec


    def _add_activated_lists(self):
        """Add packages from lists having 'activate: true' attribute"""
        for _, v in self.data.items():
            # if activated in metadata then it is a packages list
            if not v['metadata']['section'] == 'packages':
                continue

            if 'activated' not in v['metadata']:
                continue

            if not v['metadata']['activated']:
                continue

            tty.debug(f'{v}')
            spec = self._get_pe_spec(v)
            for pkg in v['packages']:
                if isinstance(pkg, dict):
                    pkg = ' '.join(self._handle_package_dictionary(pkg))

                self.pkglist.append(f'{pkg} {spec}')


    def _add_activated_pkgs(self):
        """Add packages from lists NOT having 'activate: true' attribute.
        This packages are activated using its own attribute."""
        data = self.group_sections(self.data, 'packages')

        for _, v in data.items():
            spec = self._get_pe_spec(v)
            for pkg in v['packages']:
                if not isinstance(pkg, dict):
                    continue

                if 'activated' in pkg and pkg['activated']:
                    pkg_spec = ' '.join(self._handle_package_dictionary(pkg))
                    self.pkglist.append(f'{pkg_spec} {spec}')

    def write_activated_pkgs(self):
        """Write activated packages to file, one per line"""

        with open('packages_to_activate', 'w') as f:
            for p in self.pkglist:
                f.write(p + '\n')
