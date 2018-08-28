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
from kicad.pcbnew.layer import Layer, BoardItemLayer

from kicad.util.point import Point2D

from kicad._native import _pcbnew


class Text(BoardItem):
    def __init__(self, text):
        assert isinstance(text, _pcbnew.EDA_TEXT)
        super(Text, self).__init__(text)

    def get_native(self):
        """Get native object from the low level API

        :return: :class:`pcbnew.EDA_TEXT`
        """
        return self._obj

    @property
    def layer(self):
        """layer of the drawsegment

        :return: :class:`kicad.pcbnew.Layer`
        """
        return BoardItemLayer(self._obj)

    @layer.setter
    def layer(self, layer):
        assert type(layer) is Layer
        self._obj.SetLayer(layer.id)

    @property
    def position(self):
        """Position of the Text

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxPoint(self._obj.GetPosition())

    @position.setter
    def position(self, pos):
        self._obj.SetPosition(Point2D(pos).to_wxPoint())

    @property
    def text(self):
        """Text

        :return: ``unicode``
        """
        return self._obj.GetText()

    @text.setter
    def text(self, text):
        self._obj.SetText(text)

    @property
    def text_size(self):
        """Text Size

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxSize(self._obj.GetTextSize())

    @text_size.setter
    def text_size(self, text_size):
        self._obj.SetTextSize(Point2D(text_size).to_wxSize())

    @property
    def thickness(self):
        """Thickness

        :return: ``float``
        """
        return _pcbnew.ToMM(self._obj.GetThickness())

    @thickness.setter
    def thickness(self, thickness):
        self._obj.SetThickness(_pcbnew.FromMM(thickness))

    def __repr__(self):
        return "kicad.pcbnew.Text({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Text({}, layer=\"{}\")".format(repr(self.text), self.layer.name)
