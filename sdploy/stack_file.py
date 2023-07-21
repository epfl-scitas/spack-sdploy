import os
import inspect
from jinja2 import Environment, FileSystemLoader

import llnl.util.tty as tty
import llnl.util.filesystem as fs
import spack.config
import spack.util.spack_yaml as syaml
import spack.environment as ev

from spack.util.executable import ProcessError, which

from .yaml_manager import ReadYaml

from pdb import set_trace as st

class FilterException(Exception):
    """Exception raised when filter evaluation fails"""
    def __init__(self, filter, filter_value):
        self.filter = filter
        self.filter_value = filter_value


class StackFile(ReadYaml):
    """Common opertations for Yaml files"""

    def __init__(self, config):
        """Declare class structs"""

        self.config = config

        # Configuration files
        self.platform_file = config.platform_yaml
        self.stack_file = config.stack_yaml
        self.commons_file = config.commons_yaml

        # Original data
        self.data = {} # The original data

        # Tokens are set in yaml_manager
        self.filters = {}

        # Read stack.yaml into self.data attribute
        self.read(self.stack_file)

        # Replace tokens
        self.replace_tokens(self.data)

        # Read filters
        self.filters = self.read_filters(self.platform_file)

        self.schema = None

    def _remove_newline(self, values):
        return ' '.join((values.strip().split('\n')))

    def _handle_filter(self, attributes):
        result = []
        if isinstance(attributes, dict):
            # Check for filters presence
            for fid, filter_ in self.filters.items():
                if fid in attributes:
                    if filter_ in attributes[fid]:
                        values = attributes[fid][filter_]
                        if isinstance(values, list):
                            result.extend(values)
                        else:
                            result.append(values)
                    else:
                        raise FilterException(fid, filter_)
        else:  # We are just checking that attributes is not a structure (dict, list, etc)
            # We need to cast version to str because of ' '.join in next step
            result.append(str(attributes))
        return result

    def _skip_list(self, pkg_list_cfg):
        """Returns true if the package list passed in argument is to skip

        This method searches for the presence of the 'filters' key in the
        package configuration section. If found, it will read each filter
        here defined and if at least one has the none property, this list
        is skipped."""

        if 'filters' in pkg_list_cfg:
            for filter_ in pkg_list_cfg['filters']:
                if '=' in filter_:
                    k, v = filter_.split('=')
                    if self.filters[k.strip()] != v.strip():
                        return True
                elif self.filters[filter_] == 'none':
                    return True
        return False

    def _write_yaml(self, output, filename):
        with fs.write_tmp_and_move(os.path.realpath(filename)) as f:
            yaml = syaml.load_config(output)
            if self.schema:
                spack.config.validate(yaml, self.schema, filename)
            syaml.dump_config(yaml, f, default_flow_style=False)

    def write_yaml(self, **kwargs):
        """Write yaml file"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        # Jinja setup
        file_loader = FileSystemLoader(self.templates_path)
        jinja_env = Environment(loader = file_loader, trim_blocks = True)

        # Check that template file exists in given path
        path = os.path.join(self.templates_path, self.template_file)
        if not os.path.exists(path):
            tty.die(f'Template file {self.template_file} does not exist ',
                    f'in {self.templates_path}')

        # Render and write self.yaml_file
        jinja_template = jinja_env.get_template(self.template_file)
        output = jinja_template.render(data=kwargs['data'], tokens=self.tokens)

        tty.msg(self.yaml_file)
        print(output)

        env = ev.active_environment()
        if env:
            filename = os.path.join(
                os.path.dirname(os.path.realpath(env.manifest_path)),
                self.yaml_file)
            self._write_yaml(output, filename)
        else:
            filename = os.path.join(self.yaml_path, self.yaml_file)
            tty.msg(f'Writing file {filename}')
            self._write_yaml(output, filename)

    def _define_PEs(self):
        pes = self.group_sections(self.data, 'pe')
        pe_defs = {}

        tty.debug(f'List of PEs: {pes}')

        for pe_name, pe in pes.items():
            if self._skip_list(pe):
                continue

            for stack_name, stack in pe.items():
                if stack_name in ['filters', 'metadata']:
                    continue

                tty.debug(f'{pe_name}_{stack_name}')
                pe_defs[f'{pe_name}_{stack_name}'] = {}
                res = pe_defs[f'{pe_name}_{stack_name}']
                for def_name, definition in stack.items():
                    res[def_name] = ' '.join(self._handle_filter(definition))

        return pe_defs

    def _filters_in_package(self, dic):
        """Return list of filters found in dictionary"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        result = []
        for filter in self.filters.keys():
            if filter in dic:
                result.append(filter)
        return(result)

    def _handle_package_dictionary(self, pkg_list):
        """missing docstring"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')

        if len(pkg_list.keys()) > 1:
            raise KeyError()

        pkg_name = list(pkg_list.keys())[0]
        pkg_attributes = pkg_list[pkg_name]

        try:
            package = [pkg_name]
            tty.debug(f'Reading package: {package}')

            # Do not force user to use `variants` if he only wants a filter
            for filter in self._filters_in_package(pkg_attributes):
                package.append(pkg_attributes[filter][self.filters[filter]])

            for attr in ['version', 'variants', 'dependencies']:
                if attr in pkg_attributes:
                    _spack_pkg = getattr(StackFile, '_spack_pkg_' + attr)

                    #calling self._spack_yaml_pkg_<attr>
                    package.append(_spack_pkg(self, pkg_attributes[attr]))
            return package
        except FilterException as fe:
            tty.debug(f'Ignoring package {pkg_name} in `spack.yaml` due to'
                      f'missing value for {fe.filter_value} in filter {fe.filter}')
            return None

    def _spack_pkg_version(self, version_attributes):
        """Returns package version"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        version = self._handle_filter(version_attributes)
        return(self._remove_newline(' '.join(version)))


    def _spack_pkg_variants(self, variants_attributes):
        """Returns package variants"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        variants = []
        if 'common' in variants_attributes:
            variants.append(variants_attributes['common'])

        variants.extend(self._handle_filter(variants_attributes))

        return(self._remove_newline(' '.join(variants)))

    def _spack_pkg_dependencies(self, dependencies_attributes):
        """Returns package dependencies"""

        tty.debug(f'Entering function: {inspect.stack()[0][3]}')
        dependencies = []
        # We are just checking that version_attributes is not a structure (dict, list, etc)
        if isinstance(dependencies_attributes, list):
            dependencies = dependencies_attributes
        else:
            if 'common' in dependencies_attributes:
                deps = dependencies_attributes['common']
                if not isinstance(deps, list):
                    deps = [deps]

                dependencies.extend(deps)

            dependencies.extend(self._handle_filter(dependencies_attributes))

        str_dep = ' ^'.join(dependencies)
        if str_dep:
            str_dep = ' ^' + str_dep
        return(self._remove_newline(str_dep))
