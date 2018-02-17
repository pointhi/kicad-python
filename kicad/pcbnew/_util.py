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
        raise NotImplementedError(item_type)

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
        raise NotImplementedError(item_type)

    elif item_type is _pcbnew.ZONE_CONTAINER:
        from kicad.pcbnew.zone import Zone
        return Zone(item)

    else:
        raise NotImplementedError(item_type)
