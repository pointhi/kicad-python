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

from kicad.pcbnew.layer import Layer, LayerSet

from kicad._native import _pcbnew


def from_board_item(board_item):
    item = board_item.Cast()
    item_type = type(item)

    if item_type is _pcbnew.TEXTE_PCB:
        from kicad.pcbnew.text import Text
        return Text(item)

    elif item_type is _pcbnew.BOARD:
        from kicad.pcbnew.board import Board
        return Board(item)

    elif item_type is _pcbnew.DIMENSION:
        from kicad.pcbnew.dimension import Dimension
        return Dimension(item)

    elif item_type is _pcbnew.DRAWSEGMENT:
        from kicad.pcbnew.drawsegment import Drawsegment
        return Drawsegment.from_drawsegment(item)

    elif item_type is _pcbnew.EDGE_MODULE:
        raise NotImplementedError(item_type)

    elif item_type is _pcbnew.MODULE:
        from kicad.pcbnew.module import Module
        return Module(item)

    elif item_type is _pcbnew.D_PAD:
        from kicad.pcbnew.pad import Pad
        return Pad(item)

    elif item_type is _pcbnew.TEXTE_MODULE:
        from kicad.pcbnew.text import Text
        return Text(item)

    elif item_type is _pcbnew.VIA:
        from kicad.pcbnew.text import Via
        return Via(item)

    elif item_type is _pcbnew.TRACK:
        from kicad.pcbnew.track import Track
        return Track(item)

    elif item_type is _pcbnew.PCB_TARGET:
        from kicad.pcbnew.pcbtarget import PcbTarget
        return PcbTarget(item)

    elif item_type is _pcbnew.ZONE_CONTAINER:
        from kicad.pcbnew.zone import Zone
        return Zone(item)

    else:
        raise NotImplementedError(item_type)


class BoardItem(object):
    """Create a new BoardItem object

    :param board_item: already existing board_item object
    :type board_item: :class:`pcbnew.BOARD_ITEM`
    """

    def __init__(self, board_item):
        assert isinstance(board_item, _pcbnew.BOARD_ITEM)
        self._obj = board_item

    def get_native(self):
        """Get native object from the low level API

        :return: :class:`pcbnew.BOARD_ITEM`
        """
        return self._obj

    @property
    def is_highlighted(self):
        """is highlighted?

        :return: ``bool``
        """
        return self._obj.IsHighlighted()

    @is_highlighted.setter
    def is_highlighted(self, is_highlighted):
        assert type(is_highlighted) is bool
        if is_highlighted:
            self._obj.SetHighlighted()
        else:
            self._obj.ClearHighlighted()

    @property
    def is_locked(self):
        """is locked?

        :return: ``bool``
        """
        return self._obj.IsLocked()

    @is_locked.setter
    def is_locked(self, is_locked):
        assert type(is_locked) is bool
        self._obj.SetLocked(is_locked)

    @property
    def is_selected(self):
        """is selected?

        :return: ``bool``
        """
        return self._obj.IsSelected()

    @is_selected.setter
    def is_selected(self, is_selected):
        assert type(is_selected) is bool
        if is_selected:
            self._obj.SetSelected()
        else:
            self._obj.ClearSelected()

    @property
    def layer(self):
        """primary layer of the item

        :return: ``kicad.pcbnew.Layer``
        """
        return Layer.from_id(self._obj.GetLayer())

    @property
    def layers(self):
        """All layers where the item is present on

        :return: ``kicad.pcbnew.LayerSet``
        """
        return LayerSet(self._obj.GetLayerSet())

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        if not isinstance(self._obj, other._obj.__class__):
            return False

        if self._obj == other._obj:
            return True

        if self.is_highlighted != other.is_highlighted:
            return False

        # now we will do some hack to check if the other object is actually the same. We know is_highlighted is the same
        old_value = self.is_highlighted
        self.is_highlighted = not self.is_highlighted
        is_still_same = self.is_highlighted == other.is_highlighted  # TODO: replace with something better
        self.is_highlighted = old_value
        return is_still_same

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.layers)

    def __repr__(self):
        return "kicad.pcbnew.boarditem.BoardItem({})".format(self._obj)
