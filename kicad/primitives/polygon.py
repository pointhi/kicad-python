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


class Polygon(object):
    def __init__(self):
        self._outline = []
        self._holes = []

    @property
    def outline(self):
        return self._outline

    @property
    def holes(self):
        return self._holes

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        if not isinstance(self._obj, other._obj.__class__):
            return False

        if self._obj == other._obj:
            return True

        return False  # TODO: implement real equal check

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "kicad.primitives.Polygon(outline={})".format(self._outline)


class PolygonSet(object):
    def __init__(self, poly_set=None):
        if poly_set is None:
            self._obj = _pcbnew.SHAPE_POLY_SET()
        else:
            assert isinstance(poly_set, _pcbnew.SHAPE_POLY_SET)
            self._obj = poly_set

    def get_native(self):
        """Get native object from the low level API
        :return: :class:`pcbnew.SHAPE_POLY_SET`
        """
        return self._obj

    def fracture(self):
        """Converts a set of polygons with holes to a singe outline with
        slits/fractures connecting the outer ring to the inner holes"""
        self._obj.Fracture(_pcbnew.SHAPE_POLY_SET.PM_FAST)

    def unfracture(self):
        """Converts a single outline slitted ('fractured') polygon into a set of outlines with holes"""
        self._obj.Unfracture(_pcbnew.SHAPE_POLY_SET.PM_FAST)

    def union(self, other):
        """Performs boolean PolygonSet union

        :param other: second operand of union operation
        :type other: :class:`kicad.primitives.PolygonSet`

        """
        assert isinstance(other, PolygonSet)
        self._obj.BooleanAdd(other._obj, _pcbnew.SHAPE_POLY_SET.PM_FAST)

    def difference(self, other):
        """Performs boolean PolygonSet difference

        :param other: second operand of difference operation
        :type other: :class:`kicad.primitives.PolygonSet`

        """
        assert isinstance(other, PolygonSet)
        self._obj.BooleanSubtract(other._obj, _pcbnew.SHAPE_POLY_SET.PM_FAST)

    def intersection(self, other):
        """Performs boolean PolygonSet intersection

        :param other: second operand of intersection operation
        :type other: :class:`kicad.primitives.PolygonSet`

        """
        assert isinstance(other, PolygonSet)
        self._obj.BooleanIntersection(other._obj, _pcbnew.SHAPE_POLY_SET.PM_FAST)

    def __iter__(self):
        # TODO: for the moment, we need to parse the polygon from a string, needs to be improved!!
        # Reason: it seems we cannot access the polygons using std::vector using python
        lines = iter(self._obj.Format().split('\n'))

        polygons = list()
        for _ in range(int(lines.next()[len('polyset '):])):
            new_polygon = Polygon()
            for poly in range(int(lines.next()[len('poly '):])):
                xy_coord = []  # TODO: correct type
                for _ in range(int(lines.next())):
                    xy_coord.append([_pcbnew.ToMM(int(v)) for v in lines.next().split(' ')])
                if poly == 0:
                    new_polygon._outline = xy_coord
                else:
                    new_polygon._holes.append(xy_coord)
            polygons.append(new_polygon)
            lines.next()

        # generate all polygons beforehand to prevent possible race-conditions
        for polygon in polygons:
            yield polygon

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        if not isinstance(self._obj, other._obj.__class__):
            return False

        if self._obj == other._obj:  # equal op works?
            return True

        if self._obj.checksum() != other._obj.checksum():
            return False

        return False  # TODO: implement real equal check

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "kicad.primitives.PolygonSet({})".format(self._obj)
