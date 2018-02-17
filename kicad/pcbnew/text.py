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


class Text(object):
    def __init__(self, text):
        assert isinstance(text, _pcbnew.EDA_TEXT)
        self._obj = text

    def get_native(self):
        """Get native object from the low level API

        :return: :class:`pcbnew.EDA_TEXT`
        """
        return self._obj

    @property
    def text(self):
        """Text

        :return: ``unicode``
        """
        return self._obj.GetText()

    @text.setter
    def text(self, value):
        self._obj.SetText(value)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        if not isinstance(self._obj, other._obj.__class__):
            return False

        if self._obj == other._obj:
            return True
        # TODO: SWIG has no working equal operator for objects pointing to the same object!
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "kicad.pcbnew.Text({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Text({})".format(repr(self.text))
