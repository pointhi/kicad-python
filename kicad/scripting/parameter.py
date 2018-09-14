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


class Parameter(object):
    def __init__(self, page, name, type, default, **kwargs):
        """A Parameter specifies how a specific parameter has to look like and what constrains are attached"""
        self.page = page
        self.name = name

        self.type = type
        self.default = default

        self.hint = kwargs.get('hint')  # Parameter hint (shown as mouse-over text)
        self.designator = kwargs.get('designator')  # Parameter designator such as "e, D, p" (etc)

        self.multiple = int(kwargs.get('multiple', 1))  # Check integer values are multiples of this number
        self.min_value = kwargs.get('min_value')  # Check numeric values are above or equal to this number
        self.max_value = kwargs.get('max_value')  # Check numeric values are below or equal to this number

        # TODO: custom validator

    def parse(self, value):
        parsed_value = self.type(value)
        # TODO: rangecheck
        # TODO: validation
        return parsed_value

    def __repr__(self):
        return "kicad.scripting.parameter.Parameter('{}', '{}', {}, {})".format(self.page, self.name,
                                                                                self.type, self.default)


class ParsedParameter(object):
    def __init__(self, parameter, value=None):
        self.parameter = parameter
        self._value = None

        if value is not None:
            self.value = value

    @property
    def name(self):
        return self.parameter.name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, raw_value):
        self._value = self.parameter.parse(raw_value)

    def __repr__(self):
        return "kicad.scripting.parameter.ParsedParameter('{}': '{}')".format(self.name, self.value)


class ParameterMap(object):
    def __init__(self):
        self._params = []  # sorted store
        self._params_lookup = {}  # fast lookup

    def add(self, param):
        # type: (Parameter) -> None
        if param.name in self._params_lookup:
            raise AttributeError("Parameter with name '{}' already in ParameterMap!".format(param.name))
        self._params.append(param)
        self._params_lookup[param.name] = param

    def add_parameter(self, *args, **kwargs):
        self.add(Parameter(*args, **kwargs))

    def __iter__(self):
        return self._params.__iter__()

    def __repr__(self):
        return "kicad.scripting.parameter.ParameterMap({})".format(self._params)


class ParsedParameterMap(object):
    def __init__(self, parameter_map):
        self._parameter_map = parameter_map
        self._parsed_parameters = {}

    def add(self, key, value):
        param = self._parameter_map._params_lookup[key]  # TODO
        self._parsed_parameters[key] = ParsedParameter(param, value)

    def __repr__(self):
        entries = []
        for key in self._parsed_parameters:
            value = self._parsed_parameters[key]
            entries.append('{}: {}'.format(key, repr(value.value)))
        return "kicad.scripting.parameter.ParsedParameterMap({})".format(', '.join(entries))
