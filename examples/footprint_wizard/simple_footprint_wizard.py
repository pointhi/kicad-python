#!/usr/bin/env python

from kicad.scripting import FootprintWizard, register_footprint_wizard


class ExampleWizard(FootprintWizard):
    def __init__(self):
        super(ExampleWizard, self).__init__()  # TODO: simpler design without super on current classname?

        self.name = 'Example Wizard'
        self.description = 'Example Wizard description'
        self.value = 'some_value'  # TODO: should be set in build_footprint

    def generate_parameter_list(self, params):
        params.add_parameter("Basic", "name", str, "Example_Footprint")  # TODO: float -> distance in mm
        params.add_parameter("Package", "width", float, 1)  # TODO: float -> distance in mm
        params.add_parameter("Package", "height", float, 2, designator='D')
        params.add_parameter("Package", "pad_width", float, 0.5)
        params.add_parameter("Package", "pad_height", float, 1)
        params.add_parameter("Package", "pad_spacing", float, 0.25, minValue=0.2)

    def build_footprint(self, module, params):  # TODO: create module in this method?
        # TODO: create some footprint
        return module


wizard = register_footprint_wizard(ExampleWizard)
if __name__ == '__main__':
    wizard.run_as_script()
