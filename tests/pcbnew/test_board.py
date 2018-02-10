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

import unittest

import pcbnew as kicad_pcbnew
from kicad.pcbnew import Board


class BoardTests(unittest.TestCase):

    def test_init(self):
        b = Board()
        self.assertEqual(kicad_pcbnew.BOARD, type(b.get_native()))

    def test_init_param(self):
        b_native = kicad_pcbnew.BOARD()
        b = Board(b_native)

        self.assertIs(b_native, b.get_native())
        self.assertEqual(kicad_pcbnew.BOARD, type(b.get_native()))

    def test_filepath(self):
        b = Board()
        self.assertEqual("", b.filepath)

        b.filepath = "path/to/board.kicad_mod"
        self.assertEqual("path/to/board.kicad_mod", b.filepath)
