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

from kicad.pcbnew.pad import Pad

from kicad._native import _pcbnew


class Module(object):
    def __init__(self, module):
        self._obj = module

    def get_native(self):
        # TODO: get_repr, get_native, get_internal, ...?
        return self._obj

    @staticmethod
    def from_editor():
        """Get the current module"""
        return Module(_pcbnew.GetModule())  # TODO: in footprint editor, working?

    @staticmethod
    def from_file(path):
        return Module(_pcbnew.LoadModule(path))  # TODO: working?

    @staticmethod
    def from_board(board):
        return Module(_pcbnew.MODULE(board))

    @property
    def description(self):
        """Description of the Module

        :return: ``unicode``
        """
        return self._obj.GetDescription()

    @description.setter
    def description(self, value):
        self._obj.SetDescription(value)

    @property
    def keywords(self):
        """Keywords of the Module

        :return: ``unicode``
        """
        return self._obj.GetKeywords()

    @keywords.setter
    def keywords(self, value):
        self._obj.SetKeywords(value)

    @property
    def locked(self):
        """Is Module locked?

        :return: ``bool``
        """
        return self._obj.IsLocked()

    @locked.setter
    def locked(self, value):
        self._obj.SetLocked(value)

    @property
    def pads(self):
        """List of Pads present in the Module
        
        :return: Iterator over :class:`kicad.pcbnew.Pad`
        """
        for p in self._obj.Pads():
            yield Pad(p)

    @property
    def reference(self):
        """Reference of the Module

        :return: ``unicode``
        """
        return self._obj.GetReference()

    @reference.setter
    def reference(self, value):
        self._obj.SetReference(value)

    @property
    def value(self):
        """Value of the Module
        
        :return: ``unicode``
        """
        return self._obj.GetValue()

    @value.setter
    def value(self, value):
        self._obj.SetValue(value)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        if not isinstance(self._obj, other._obj.__class__):
            return False

        if self._obj == other._obj:
            return True

        if self.reference != other.reference:
            return False

        # now we will do some hack to check if the other object is actually the same. We know reference is the same
        old_reference = self.reference
        self.reference += "_eqal_test"
        is_still_same = self.reference == other.reference  # TODO: replace with something better than a hack
        self.reference = old_reference
        return is_still_same

    def __repr__(self):
        return "kicad.pcbnew.Module({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Module(\"{}\")".format(self.reference)
