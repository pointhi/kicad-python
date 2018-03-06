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


# dict for default layers to convert layer names to id and back
_LAYERS = {_pcbnew.BOARD_GetStandardLayerName(n): n for n in range(_pcbnew.PCB_LAYER_ID_COUNT)}
_LAYERS_NAME_LOOKUP = {s: n for n, s in _LAYERS.iteritems()}


class Layer(object):
    def __init__(self, id):
        assert type(id) is int
        self._id = id

    @staticmethod
    def from_id(id):
        """Get Layer object from id

        :param id:
        :type id: ``int``

        :return: :class:`kicad.pcbnew.Layer`
        """
        return Layer(id)

    @staticmethod
    def from_name(name):
        """Get Layer object from name

        :param name:
        :type id: ``str``, ``unicode``

        :return: :class:`kicad.pcbnew.Layer`
        """
        assert type(name) in [str, unicode]
        return Layer(_LAYERS[name])

    @property
    def id(self):
        """internal ID of the layer

        :return: ``int``
        """
        return self._id

    @id.setter
    def id(self, id):
        assert type(id) is int
        self._id = id

    @property
    def name(self):
        """name of the layer

        :return: ``unicode``
        """
        return _LAYERS_NAME_LOOKUP.get(self._id, "")

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        return self.id == other.id and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "kicad.pcbnew.Layer(id={})".format(self.id)

    def __str__(self):
        return "kicad.pcbnew.Layer(id={}, name=\"{}\")".format(self.id, self.name)


class BoardItemLayer(Layer):
    def __init__(self, board_item):
        assert isinstance(board_item, _pcbnew.BOARD_ITEM)
        self._obj = board_item

    @property
    def id(self):
        """internal ID of the layer

        :return: ``int``
        """
        return self._obj.GetLayer()

    @id.setter
    def id(self, id):
        assert type(id) is int
        self._obj.SetLayer(id)

    @property
    def name(self):
        """name of the layer

        :return: ``unicode``
        """
        return self._obj.GetLayerName()
