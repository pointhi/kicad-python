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


class Pad(object):
    def __init__(self, pad):
        self._obj = pad

    def get_native(self):
        # TODO: get_repr, get_native, get_internal, ...?
        return self._obj

    @property
    def name(self):
        """Name of the Pad

        :return: ``unicode``
        """
        return self._obj.GetName()

    @name.setter
    def name(self, value):
        self._obj.SetName(value)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        if not isinstance(self._obj, other._obj.__class__):
            return False

        if self._obj == other._obj:
            return True

        if self.name != other.name:
            return False

        # now we will do some hack to check if the other object is actually the same. We know name is the same
        old_name = self.name
        self.name += "_eqal_test"
        is_still_same = self.name == other.name  # TODO: replace with something better than a hack
        self.name = old_name
        return is_still_same

    def __repr__(self):
        return "kicad.pcbnew.Pad({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Pad(\"{}\")".format(self.name)
