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

import sys

from kicad.pcbnew.board import Board
from kicad.pcbnew.layer import Layer

from kicad._native import _pcbnew


# https://stackoverflow.com/questions/43645628/how-to-plot-colored-output-from-pcbnew-via-python-scripting
# https://scottbezek.blogspot.co.at/2016/04/scripting-kicad-pcbnew-exports.html

class Plotter(object):
    PLOT_FORMAT_HPGL = _pcbnew.PLOT_FORMAT_HPGL
    PLOT_FORMAT_GERBER = _pcbnew.PLOT_FORMAT_GERBER
    PLOT_FORMAT_POSTSCRIPT = _pcbnew.PLOT_FORMAT_POST
    PLOT_FORMAT_DXF = _pcbnew.PLOT_FORMAT_DXF
    PLOT_FORMAT_PDF = _pcbnew.PLOT_FORMAT_PDF
    PLOT_FORMAT_SVG = _pcbnew.PLOT_FORMAT_SVG

    def __init__(self, board, layer=None, color_mode=None):
        assert type(board) is Board

        self._board = board
        self._pctl = _pcbnew.PLOT_CONTROLLER(self._board.get_native())
        self._popt = self._pctl.GetPlotOptions()

        if layer is not None:
            self.layer = layer

        if color_mode is not None:
            self.color_mode = color_mode

    def open(self, filename, format, sheet_description=None):
        """Open a new plotfile for writing

        :param filename: Name of the file to plot
        :type filename: ``str``
        :param format: format of the output file
        :param sheet_description: some description

        :return: :class:`kicad.plotter.Plotter`

        :Example:

        >>> from kicad.pcbnew import Board, Layer
        >>> from kicad.plotter import Plotter
        >>> b = Board.from_editor()
        >>> p = Plotter(b, layer=Layer.from_id(0))
        >>> with p.open('test', Plotter.PLOT_FORMAT_SVG):
        ...     p.plot_layer()# doctest: +SKIP
        ...
        """
        if sys.version_info >= (3,):
            assert type(filename) is str
            assert sheet_description is None or type(sheet_description) is str
        else:
            assert type(filename) in [str, unicode]
            assert sheet_description is None or type(sheet_description) in [str, unicode]

        self._pctl.OpenPlotfile(filename, format, sheet_description)

        return self  # to support "__enter__"

    def close(self):
        """Close a plotfile after writing

        :Example:

        >>> from kicad.pcbnew import Board, Layer
        >>> from kicad.plotter import Plotter
        >>> b = Board.from_editor()
        >>> p = Plotter(b, layer=Layer.from_id(0))
        >>> p.open('test', Plotter.PLOT_FORMAT_SVG)
        kicad.plotter.Plotter(board="")
        >>> p.plot_layer()# doctest: +SKIP
        >>> p.close()
        """
        self._pctl.ClosePlot()

    @property
    def color_mode(self):
        """is color mode enabled?

        :return: ``bool``
        """
        return self._pctl.GetColorMode()

    @color_mode.setter
    def color_mode(self, color_mode):
        assert type(color_mode) is bool
        self._pctl.SetColorMode(color_mode)

    @property
    def is_open(self):
        """is plotfile open?

        :return: ``bool``
        """
        return self._pctl.IsPlotOpen()

    @property
    def layer(self):
        """layer to plot on

        :return: :class:`kicad.pcbnew.Layer`
        """
        return Layer.from_id(self._pctl.GetLayer())

    @layer.setter
    def layer(self, layer):
        assert type(layer) is Layer
        self._pctl.SetLayer(layer.id)

    def plot_layer(self):
        """plot layer to opened file"""
        self._pctl.PlotLayer()

    def __enter__(self):
        # TODO: this only works with the open statement
        if not self.is_open:
            raise RuntimeError("You have to use \"Plot.open(...)\" as defined in the documentation")
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __repr__(self):
        return "kicad.plotter.Plotter(board=\"{}\")".format(self._board.filepath)

    def __str__(self):
        return "kicad.plotter.Plotter(layer=\"{}\")".format(self.layer.name)
