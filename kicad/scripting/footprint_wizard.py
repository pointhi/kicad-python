# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# (C) 2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import argparse
import os
import sys

try:
    import yaml
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False

from kicad.scripting.parameter import ParameterMap, ParsedParameterMap

from kicad.pcbnew import Module
from kicad._native import _pcbnew


class FootprintWizard(object):
    def __init__(self):
        self.name = "KiCad FP Wizard"
        self.description = "Undefined Footprint Wizard plugin"
        self.image = ""
        self.value = ""
        self.reference_prefix = "REF"

    def generate_parameter_list(self, params):
        # type: (ParameterMap) -> None
        raise NotImplementedError("generate_parameter_list is not implemented!")

    def build_footprint(self, module, params):
        # type: (Module, ParsedParameterMap) -> Module
        raise NotImplementedError("build_footprint is not implemented!")


# https://github.com/KiCad/kicad-source-mirror/blob/master/pcbnew/python/plugins/FootprintWizardBase.py
# https://github.com/KiCad/kicad-source-mirror/blob/72f87861bb22bf2ecb82ea570d9828a287436748/scripting/kicadplugins.i#L478  # noqa
class _FootprintWizardBase(_pcbnew.FootprintWizardPlugin):
    UNIT_CONVERSATION_TABLE = {
        bool: _pcbnew.uBool,
        int: _pcbnew.uInteger,
        float: _pcbnew.uFloat,
        str: _pcbnew.uString
    }  # TODO: support more units

    def __init__(self, footprint_wizard):
        super(_FootprintWizardBase, self).__init__()

        self.fp_wz = footprint_wizard

        self.GenerateParameterList()

    def GetName(self):  # Return the name of this wizard
        return self.fp_wz.name

    def GetImage(self):  # Return the filename of the preview image associated with this wizard
        return self.fp_wz.image

    def GetDescription(self):  # Return the description text
        return self.fp_wz.description

    def GetValue(self):
        return self.fp_wz.value

    def GetReferencePrefix(self):
        return self.fp_wz.reference_prefix

    def GenerateParameterList(self):
        params = ParameterMap()
        self.fp_wz.generate_parameter_list(params)

        for p in params:
            kwargs = {}
            if p.hint is not None:
                kwargs['hint'] = p.hint
            if p.designator is not None:
                kwargs['designator'] = p.designator
            if p.multiple is not None:
                kwargs['multiple'] = p.multiple
            if p.min_value is not None:
                kwargs['min_value'] = p.min_value
            if p.max_value is not None:
                kwargs['max_value'] = p.max_value

            unit = _FootprintWizardBase.UNIT_CONVERSATION_TABLE.get(p.type, _pcbnew.uString)
            self.AddParam(p.page, p.name, unit, p.default, **kwargs)

    def BuildFootprint(self):
        # reset variables which are used by footprint wizard
        self.buildmessages = ''
        self.module = _pcbnew.MODULE(None)

        module = Module(self.module)

        self.buildmessages += 'Building new {} footprint with the following parameters:\n'.format(self.GetName())

        params = ParameterMap()
        self.fp_wz.generate_parameter_list(params)

        fp_params = ParsedParameterMap(params)

        for page in self.parameters:
            self.buildmessages += '{}\n'.format(page)
            parameters = self.parameters[page]
            for key in parameters:
                value = parameters[key]
                self.buildmessages += '\t{} = {}\n'.format(key, value)
                fp_params.add(key, value)

        module.value = self.fp_wz.value
        module.reference = "{}**".format(self.fp_wz.reference_prefix)

        fpid = _pcbnew.LIB_ID("", module.value)  # the lib name  (empty) and the name in library
        module.get_native().SetFPID(fpid)

        self.fp_wz.build_footprint(module, fp_params)


class FootprintScriptingWizard(object):
    def __init__(self, wizard_class):
        # TODO: test if class can be created
        self.wizard_class = wizard_class

    def create(self):
        # type: () -> FootprintWizard
        """Create a new object of the given wizard class"""
        return self.wizard_class()

    def run_as_script(self):
        # type: () -> None
        """Run wizard from the command line"""
        wizard = self.create()
        params = ParameterMap()
        wizard.generate_parameter_list(params)

        parser = argparse.ArgumentParser(description=wizard.description)

        # parser.add_argument('--specifications', type=argparse.FileType('r'), nargs='*',
        #                    help='config files defining how the footprint will look like')
        parser.add_argument('definitions', type=argparse.FileType('r'), nargs='+',
                            help='config files defining the footprint properties')
        parser.add_argument('--library', type=str, default='.',
                            help='library path where to store the footprints')
        parser.add_argument('--dry-run', action='store_true',
                            help='do not save the generated footprints')

        args = parser.parse_args()

        if not os.path.isdir(args.library):
            parser.error('"{}" is not a valid directory'.format(args.library))

        if not _YAML_AVAILABLE:
            parser.error('PyYAML is required to be installed')

        for definition in args.definitions:
            param_generator = self.parse_yaml(params, definition)
            for fp_params in param_generator:
                print(fp_params)
                # TODO: duplicate with _FootprintWizardBase
                module = Module(_pcbnew.MODULE(None))

                module.value = wizard.value  # TODO: name?
                module.reference = "{}**".format(wizard.reference_prefix)

                fpid = _pcbnew.LIB_ID("", module.value)  # the lib name  (empty) and the name in library
                module.get_native().SetFPID(fpid)

                wizard.build_footprint(module, fp_params)

                fp_name = '{}.kicad_mod'.format(module.get_native().GetFPID().GetLibItemName())
                print('* Footprint generated: "{}"'.format(os.path.join(args.library, fp_name)))

                if not args.dry_run:
                    module.to_library(args.library)

    def parse_yaml(self, params, definition):
        if not _YAML_AVAILABLE:
            print("pyyaml not available!")
            sys.exit(1)

        parsed = yaml.load(definition)

        for config in parsed:
            fp_params = ParsedParameterMap(params)
            for key in config:
                value = config[key]
                fp_params.add(key, value)
            # TODO: validate
            yield fp_params


def register_footprint_wizard(wizard_class):
    # create object and register as footprint wizard
    registered_wizard = wizard_class()
    registered_wizard_base = _FootprintWizardBase(registered_wizard)
    registered_wizard_base.register()

    return FootprintScriptingWizard(wizard_class)
