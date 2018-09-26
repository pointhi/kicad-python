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

from kicad.pcbnew.boarditem import BoardItem
from kicad.pcbnew.net import Net

from kicad.util.point import Point2D

from kicad._native import _pcbnew


class Pad(BoardItem):
    def __init__(self, pad):
        assert isinstance(pad, _pcbnew.D_PAD)
        super(Pad, self).__init__(pad)

    def get_native(self):
        """Get native object from the low level API

        :return: :class:`pcbnew.PAD`
        """
        return self._obj

    @property
    def name(self):
        """Name of the Pad

        :return: ``unicode``
        """
        return self._obj.GetName()

    @name.setter
    def name(self, name):
        self._obj.SetName(name)

    @property
    def drill_size(self):
        """Drill size of the Pad

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxPoint(self._obj.GetDrillSize())

    @drill_size.setter
    def drill_size(self, drill_size):
        self._obj.SetDrillSize(Point2D(drill_size).to_wxSize())

    @property
    def size(self):
        """Size of the Pad

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxPoint(self._obj.GetSize())

    @size.setter
    def size(self, size):
        self._obj.SetSize(Point2D(size).to_wxSize())

    @property
    def net(self):
        """Net of the Zone

        :return: :class:`kicad.pcbnew.Net`
        """
        return Net(self._obj.GetNet())

    def __repr__(self):
        return "kicad.pcbnew.Pad({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Pad(\"{}\")".format(self.name)
