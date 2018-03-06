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
from kicad.pcbnew.layer import Layer, BoardItemLayer

from kicad.util.point import Point2D

from kicad._native import _pcbnew


class Drawsegment(BoardItem):
    def __init__(self, drawsegment):
        assert isinstance(drawsegment, _pcbnew.DRAWSEGMENT)
        super(Drawsegment, self).__init__(drawsegment)

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
        elif shape is _pcbnew.S_POLYGON:
            return Polygon(drawsegment)
        # elif shape is _pcbnew.S_CURVE:
        #    return Curve(drawsegment)
        else:
            raise NotImplementedError(drawsegment.GetShapeStr())

    @property
    def layer(self):
        """layer of the drawsegment

        :return: :class:`kicad.pcbnew.Layer`
        """
        return BoardItemLayer(self._obj)

    @layer.setter
    def layer(self, layer):
        assert type(layer) is Layer
        self._obj.SetLayer(layer.id)

    @property
    def width(self):
        """Width of line in mm

        :return: ``float``
        """
        return _pcbnew.ToMM(self._obj.GetWidth())

    @width.setter
    def width(self, width):
        self._obj.SetWidth(_pcbnew.FromMM(width))

    def __repr__(self):
        return "kicad.pcbnew.Drawsegment({})".format(self._obj)


class Arc(Drawsegment):
    def __init__(self, arc):
        assert arc.GetShape() is _pcbnew.S_ARC
        super(Arc, self).__init__(arc)

    @property
    def angle(self):
        """angle of arc in degree

        :return: ``float``
        """
        return self._obj.GetAngle() / 10.

    @angle.setter
    def angle(self, angle):
        assert type(angle) in [int, float]
        self._obj.SetAngle(angle * 10.)

    @property
    def center(self):
        """Center point of arc

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxPoint(self._obj.GetCenter())

    @center.setter
    def center(self, center):
        self._obj.SetCenter(Point2D(center).to_wxPoint())

    @property
    def start(self):
        """Start point of arc

        :return: :class:`kicad.util.Point2D`
        """
        return Point2D.from_wxPoint(self._obj.GetStart())

    @start.setter
    def start(self, start):
        self._obj.SetStart(Point2D(start).to_wxPoint())

    def __repr__(self):
        return "kicad.pcbnew.Arc({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Arc(center={}, start={}, angle={}, width={}, layer=\"{}\")".format(self.center,
                                                                                                self.start,
                                                                                                self.angle,
                                                                                                self.width,
                                                                                                self.layer.name)


class Circle(Drawsegment):
    def __init__(self, circle):
        assert circle.GetShape() is _pcbnew.S_CIRCLE
        super(Circle, self).__init__(circle)

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
        return max(abs(diff.x), abs(diff.y))

    @radius.setter
    def radius(self, radius):
        point2d_radius = self.center + Point2D(radius, radius)
        self._obj.SetCenter(point2d_radius.to_wxPoint())

    def __repr__(self):
        return "kicad.pcbnew.Circle({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Circle(center={}, diameter={}, width={}, layer=\"{}\")".format(self.center,
                                                                                            self.diameter,
                                                                                            self.width,
                                                                                            self.layer.name)


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

    def __repr__(self):
        return "kicad.pcbnew.Line({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Line(start={}, end={}, width={}, layer=\"{}\")".format(self.start,
                                                                                    self.end,
                                                                                    self.width,
                                                                                    self.layer.name)


class Polygon(Drawsegment):
    def __init__(self, polygon):
        assert polygon.GetShape() is _pcbnew.S_POLYGON
        super(Polygon, self).__init__(polygon)

    def __repr__(self):
        return "kicad.pcbnew.Polygon({})".format(self._obj)

    def __str__(self):
        return "kicad.pcbnew.Polygon(layer=\"{}\")".format(self.layer.name)
