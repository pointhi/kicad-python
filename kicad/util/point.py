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


class Point2D(object):
    """Representation of a 2D Point in space

    :Example:

    >>> from kicad.util.point import Point2D
    >>> Point2D(0, 1)
    kicad.util.point.Point2D(0.0, 1.0)
    >>> Point2D([2, 3])
    kicad.util.point.Point2D(2.0, 3.0)
    >>> Point2D((4, 5))
    kicad.util.point.Point2D(4.0, 5.0)
    >>> Point2D({'x': 6, 'y':7})
    kicad.util.point.Point2D(6.0, 7.0)
    >>> Point2D(Point2D(8, 9))
    kicad.util.point.Point2D(8.0, 9.0)
    """
    def __init__(self, coordinates=None, y=None):
        # parse constructor
        if coordinates is None:
            coordinates = {}
        elif type(coordinates) in [int, float]:
            if y is not None:
                coordinates = [coordinates, y]
            else:
                raise TypeError('you have to give x and y coordinate')
        elif isinstance(coordinates, Point2D):
            coordinates = coordinates.__dict__()

        # parse points with format: Point2D({'x':0, 'y':0})
        if type(coordinates) is dict:
            self.x = float(coordinates.get('x', 0.))
            self.y = float(coordinates.get('y', 0.))
            return

        # parse points with format: Point2D([0, 0]) or Point2D((0, 0))
        if type(coordinates) in [list, tuple]:
            if len(coordinates) == 2:
                self.x = float(coordinates[0])
                self.y = float(coordinates[1])
                return
            else:
                raise TypeError('invalid list size (2 elements expected)')

        raise TypeError('invalid parameters given')

    @staticmethod
    def from_wxPoint(wxobj):
        """Convert a wxPoint to a Point2D

        :param wxobj: point to convert
        :type wxobj: :class:`pcbnew.wxPoint`

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D(_pcbnew.ToMM(wxobj))

    @staticmethod
    def from_wxSize(wxobj):
        """Convert a wxSize to a Point2D

        :param wxobj: point to convert
        :type wxobj: :class:`pcbnew.wxSize`

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D(_pcbnew.ToMM(wxobj))

    def to_wxPoint(self):
        """Convert coordinate to internal coordinate

        :return: :class:`pcbnew.wxPoint`
        """
        return _pcbnew.wxPointMM(float(self.x), float(self.y))

    def to_wxSize(self):
        """Convert size given as Point2D to internal size

        :return: :class:`pcbnew.wxSize`
        """
        return _pcbnew.wxSizeMM(float(self.x), float(self.y))

    def round_to(self, base, prec=10):
        """Round to a specific base (like it's required for a grid)

        :param base: base we want to round to
        :type base: ``float``
        :param prec: precision of rounding operation
        :type prec: ``int``

        :return: :class:`kicad.util.Point2D`

        :Example:

        >>> from kicad.util.point import Point2D
        >>> Point2D(0.1234, 0.5678).round_to(0.01)
        kicad.util.point.Point2D(0.12, 0.57)
        """
        if base == 0:
            return self

        return Point2D({'x': round(base * round(self.x / base), prec),
                        'y': round(base * round(self.y / base), prec)})

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def __arithmetic_parse(value):
        if isinstance(value, Point2D):
            return value
        elif type(value) in [int, float]:
            return Point2D([value, value])
        else:
            return Point2D(value)

    def __add__(self, value):
        other = Point2D.__arithmetic_parse(value)

        return Point2D({'x': self.x + other.x,
                        'y': self.y + other.y})

    def __sub__(self, value):
        other = Point2D.__arithmetic_parse(value)

        return Point2D({'x': self.x - other.x,
                        'y': self.y - other.y})

    def __mul__(self, value):
        other = Point2D.__arithmetic_parse(value)

        return Point2D({'x': self.x * other.x,
                        'y': self.y * other.y})

    def __div__(self, value):
        other = Point2D.__arithmetic_parse(value)

        return Point2D({'x': self.x / other.x,
                        'y': self.y / other.y})

    def __truediv__(self, obj):
        return self.__div__(obj)

    def __dict__(self):
        return {'x': self.x, 'y': self.y}

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "kicad.util.point.Point2D({x}, {y})".format(**self.__dict__())

    def __str__(self):
        return "[{x}, {y}]".format(**self.__dict__())
