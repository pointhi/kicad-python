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

from kicad.util.point import Point2D

from kicad._native import _pcbnew


class PcbTarget(BoardItem):  # TODO: better name?, is used for layer alignment
    def __init__(self, target):
        assert isinstance(target, _pcbnew.PCB_TARGET)
        super(PcbTarget, self).__init__(target)

    def get_native(self):
        """Get native object from the low level API

        :return: :class:`pcbnew.EDA_TEXT`
        """
        return self._obj

    @property
    def position(self):
        """position of the PcbTarget

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxPoint(self._obj.GetPosition())

    @position.setter
    def position(self, center):
        self._obj.SetPosition(Point2D(center).to_wxPoint())

    @property
    def width(self):
        """Width of line in mm

        :return: ``float``
        """
        return _pcbnew.ToMM(self._obj.GetWidth())

    @width.setter
    def width(self, width):
        self._obj.SetWidth(_pcbnew.FromMM(width))

    def __repr__(self):
        return "kicad.pcbnew.PcbTarget({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.PcbTarget(position={}, width={})".format(self.position, self.width)
