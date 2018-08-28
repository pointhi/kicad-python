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


class Net(object):
    def __init__(self, netinfo):
        assert isinstance(netinfo, _pcbnew.NETINFO_ITEM)
        self._obj = netinfo

    def get_native(self):
        """Get native object from the low level API

        :return: :class:`pcbnew.NETINFO_ITEM`
        """
        return self._obj

    @property
    def name(self):
        """Name of Net

        :return: ``unicode``
        """
        return self._obj.GetNetname()

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        if not isinstance(self._obj, other._obj.__class__):
            return False

        if self._obj == other._obj:
            return True

        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "kicad.pcbnew.Net({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Net(\"{}\")".format(self.name)
