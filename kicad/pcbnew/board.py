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

from .drawing import Drawing
from .module import Module
from .track import Track
from .zone import Zone

_pcbnew = __import__('pcbnew')  # We need to import the pcbnew module this way, otherwise we try to import us ourself


class Board(object):
    def __init__(self, board=None):
        if board is None:
            board = _pcbnew.BOARD()

        self._obj = board

    def get_native(self):
        # TODO: get_repr, get_native, get_internal, ...?
        return self._obj

    @staticmethod
    def from_editor():
        """Get the current board"""
        return Board(_pcbnew.GetBoard())

    @staticmethod
    def from_file(path):
        return Board(_pcbnew.LoadBoard(path))

    @staticmethod
    def from_source(source):
        pass  # TODO: missing

    def save(self):
        pass  # TODO: missing

    def export(self, path, type):
        pass  # TODO: missing

    @property
    def filename(self):
        return self._obj.GetFileName()

    @filename.setter
    def filename(self, filename):
        self._obj.SetFileName(filename)

    @property
    def aux_origin(self):
        return self._obj.GetAuxOrigin()  # TODO: format conversation?

    @aux_origin.setter
    def aux_origin(self, origin):
        self._obj.SetAuxOrigin(origin)  # TODO: format conversation?

    @property
    def grid_origin(self):
        return self._obj.GetGridOrigin()  # TODO: format conversation?

    @grid_origin.setter
    def grid_origin(self, origin):
        self._obj.SetGridOrigin(origin)  # TODO: format conversation?

    @property
    def modules(self):
        it = self._obj.GetModules().begin()  # TODO: check
        while not it == None:
            yield Module(it)
            it = it.Next()

    @property
    def tracks(self):
        it = self._obj.GetTracks().begin()  # TODO: check
        while not it == None:
            yield Track(it)  # TODO: vias also included
            it = it.Next()

    @property
    def zones(self):
        it = self._obj.GetZones().begin()  # TODO: check
        while not it == None:
            yield Zone(it)
            it = it.Next()

    def is_zone_filled(self):
        pass  # TODO: implement

    def zone_fill(self):
        pass  # TODO: implement

    def zone_unfill(self):
        pass  # TODO: implement

    @property
    def drawings(self):
        it = self._obj.GetDrawings().begin()  # TODO: check
        while not it == None:
            yield Drawing(it)
            it = it.Next()

    @property
    def layers_enabled(self):
        return self._obj.GetEnabledLayers()  # TODO: add wrapper and setter
