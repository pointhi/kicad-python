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

from typing import Generator  # noqa: F401

from kicad.pcbnew.boarditem import BoardItem

from kicad.pcbnew.pad import Pad

from kicad.util.point import Point2D

from kicad._native import _pcbnew


class Module(BoardItem):
    def __init__(self, module):
        # type: (_pcbnew.MODULE) -> None
        assert isinstance(module, _pcbnew.MODULE)
        super(Module, self).__init__(module)

    def get_native(self):
        # type: () -> _pcbnew.MODULE
        """Get native object from the low level API

        :return: :class:`pcbnew.MODULE`
        """
        return self._obj

    @staticmethod
    def from_library(lib_path, name):
        # type: (str, str) -> Module
        """Load Module from library

        :param lib_path: library path
        :type lib_path: ``str``, ``unicode``
        :param name: name of the footprin to load
        :type name: ``str``, ``unicode``

        :return: :class:`pcbnew.MODULE`
        """
        io = _pcbnew.PCB_IO()
        return Module(io.FootprintLoad(lib_path, name))

    def to_library(self, lib_path):
        # type: (str) -> None
        """Save Module to library

        :param lib_path: library path where to save the footprint
        :type lib_path: ``str``, ``unicode``
        """
        io = _pcbnew.PCB_IO()
        io.FootprintSave(lib_path, self.get_native())  # TODO: uses FPID().GetLibItemName(), what to do when not set?

    @property
    def description(self):
        # type: () -> str
        """Description of the Module

        :return: ``unicode``
        """
        return self._obj.GetDescription()

    @description.setter
    def description(self, description):
        # type: (str) -> None
        self._obj.SetDescription(description)

    @property
    def keywords(self):
        # type: () -> str
        """Keywords of the Module

        :return: ``unicode``
        """
        return self._obj.GetKeywords()

    @keywords.setter
    def keywords(self, keywords):
        # type: (str) -> None
        self._obj.SetKeywords(keywords)

    @property
    def pads(self):
        # type: () -> Generator[Pad, None, None]
        """List of Pads present in the Module

        :return: Iterator over :class:`kicad.pcbnew.Pad`
        """
        for p in self._obj.Pads():
            yield Pad(p)

    @property
    def position(self):
        # type: () -> Point2D
        """Position of the Module

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxPoint(self._obj.GetPosition())

    @position.setter
    def position(self, pos):
        self._obj.SetPosition(Point2D(pos).to_wxPoint())

    @property
    def reference(self):
        # type: () -> str
        """Reference of the Module

        :return: ``unicode``
        """
        return self._obj.GetReference()

    @reference.setter
    def reference(self, reference):
        # type: (str) -> None
        self._obj.SetReference(reference)

    @property
    def value(self):
        # type: () -> str
        """Value of the Module

        :return: ``unicode``
        """
        return self._obj.GetValue()

    @value.setter
    def value(self, value):
        # type: (str) -> None
        self._obj.SetValue(value)

    def __repr__(self):
        # type: () -> str
        return "kicad.pcbnew.Module({})".format(self._obj)

    def __str__(self):
        # type: () -> str
        return "kicad.pcbnew.Module(\"{}\")".format(self.reference)
