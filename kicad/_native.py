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

try:
    _pcbnew = __import__('pcbnew')  # We need to import the pcbnew module this way
except ImportError as e:
    if 'sphinx' not in sys.modules:
        raise e
    else:
        class PcbnewDummy(object):
            PCB_LAYER_ID_COUNT = 0
            PLOT_FORMAT_HPGL = None
            PLOT_FORMAT_GERBER = None
            PLOT_FORMAT_POST = None
            PLOT_FORMAT_DXF = None
            PLOT_FORMAT_PDF = None
            PLOT_FORMAT_SVG = None

        _pcbnew = PcbnewDummy()
