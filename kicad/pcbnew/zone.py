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

from kicad._native import _pcbnew


class Zone(BoardItem):
    def __init__(self, zone):
        assert isinstance(zone, _pcbnew.ZONE_CONTAINER)
        super(Zone, self).__init__(zone)

    def get_native(self):
        """Get native object from the low level API

        :return: :class:`pcbnew.ZONE`
        """
        return self._obj

    @property
    def priority(self):
        """Priority of the Zone

        :return: ``int``
        """
        return self._obj.GetPriority()

    @priority.setter
    def priority(self, priority):
        self._obj.SetPriority(priority)

    @property
    def net(self):
        """Net of the Zone

        :return: :class:`kicad.pcbnew.Net`
        """
        return Net(self._obj.GetNet())

    def __repr__(self):
        return "kicad.pcbnew.Zone({})".format(self._obj)
