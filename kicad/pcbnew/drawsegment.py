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

from kicad.util.point import Point2D

from kicad._native import _pcbnew


class Drawsegment(object):
    def __init__(self, drawsegment):
        assert isinstance(drawsegment, _pcbnew.DRAWSEGMENT)
        self._obj = drawsegment

    def get_native(self):
        """Get native object from the low level API

        :return: :class:`pcbnew.DRAWSEGMENT`
        """
        return self._obj

    @staticmethod
    def from_drawsegment(drawsegment):
        assert isinstance(drawsegment, _pcbnew.DRAWSEGMENT)

        shape = drawsegment.GetShape()

        if shape is _pcbnew.S_SEGMENT:
            return Line(drawsegment)
        # elif shape is _pcbnew.S_RECT:
        #    return Rect(drawsegment)
        elif shape is _pcbnew.S_ARC:
            return Arc(drawsegment)
        elif shape is _pcbnew.S_CIRCLE:
            return Circle(drawsegment)
        # elif shape is _pcbnew.S_POLYGON:
        #    return Polygone(drawsegment)
        # elif shape is _pcbnew.S_CURVE:
        #    return Curve(drawsegment)
        else:
            raise NotImplementedError(drawsegment.GetShapeStr())


class Line(Drawsegment):
    def __init__(self, line):
        assert line.GetShape() is _pcbnew.S_SEGMENT
        super(Line, self).__init__(line)

    @property
    def start(self):
        """Start point of line

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxPoint(self._obj.GetStart())

    @start.setter
    def start(self, start):
        self._obj.SetStart(Point2D(start).to_wxPoint())

    @property
    def end(self):
        """End point of line

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxPoint(self._obj.GetEnd())

    @end.setter
    def end(self, end):
        self._obj.SetEnd(Point2D(end).to_wxPoint())

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        if not isinstance(self._obj, other._obj.__class__):
            return False

        if self._obj == other._obj:
            return True

        if not self.start == other.start:
            return False

        if self.end != other.end:
            return False

        # now we will do some hack to check if the other object is actually the same. We know start is the same
        old_start = self.start
        self.start += [0.1, 0]
        is_still_same = self.start == other.start  # TODO: replace with something better than a hack
        self.start = old_start
        return is_still_same

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "kicad.pcbnew.Line({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Line(start={}, end={})".format(self.start, self.end)


class Arc(Drawsegment):
    def __init__(self, arc):
        assert arc.GetShape() is _pcbnew.S_ARC
        super(Line, self).__init__(arc)

    def __repr__(self):
        return "kicad.pcbnew.Arc({})".format(self._obj)


class Circle(Drawsegment):
    def __init__(self, circle):
        assert circle.GetShape() is _pcbnew.S_CIRCLE
        super(Line, self).__init__(circle)

    @property
    def center(self):
        """Center point of circle

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxPoint(self._obj.GetCenter())

    @center.setter
    def center(self, center):
        self._obj.SetCenter(Point2D(center).to_wxPoint())

    @property
    def diameter(self):
        """Diameter of circle

        :return: ``float``
        """
        return self.radius * 2.0

    @diameter.setter
    def diameter(self, diameter):
        self.radius = diameter / 2.0

    @property
    def radius(self):
        """Radius of circle

        :return: ``float``
        """
        end = Point2D.from_wxPoint(self._obj.GetEnd())
        diff = self.center - end
        return min(diff.x, diff.y)

    @radius.setter
    def radius(self, radius):
        point2d_radius = self.center + Point2D(radius, radius)
        self._obj.SetCenter(point2d_radius.to_wxPoint())

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        if not isinstance(self._obj, other._obj.__class__):
            return False

        if self._obj == other._obj:
            return True

        if not self.center == other.center:
            return False

        if self.radius != other.radius:
            return False

        # now we will do some hack to check if the other object is actually the same. We know center is the same
        old_center = self.center
        self.center += [0.1, 0]
        is_still_same = self.center == other.center  # TODO: replace with something better than a hack
        self.center = old_center
        return is_still_same

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "kicad.pcbnew.Circle({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Circle(center={}, diameter={})".format(self.center, self.diameter)
