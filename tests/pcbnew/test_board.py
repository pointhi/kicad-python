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
import os

import pcbnew as _pcbnew
from kicad.pcbnew import Board


TEST_PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testproject')
TEST_PROJECT_FILE = os.path.join(TEST_PROJECT_DIR, 'testproject.kicad_pcb')


class BoardTests(unittest.TestCase):

    def test_init(self):
        b = Board()
        self.assertEqual(_pcbnew.BOARD, type(b.get_native()))

    def test_from_file(self):
        b = Board.from_file(TEST_PROJECT_FILE)
        self.assertEqual(TEST_PROJECT_FILE, b.filepath)

    def test_from_file_not_existing(self):
        self.assertRaises(IOError, Board.from_file, os.path.join(TEST_PROJECT_DIR, 'not_existing.kicad_pcb'))

    def test_from_file_invalid(self):
        self.assertRaises(IOError, Board.from_file, os.path.join(TEST_PROJECT_DIR, 'testproject.pro'))

    def test_init_param(self):
        b_native = _pcbnew.BOARD()
        b = Board(b_native)

        self.assertIs(b_native, b.get_native())
        self.assertEqual(_pcbnew.BOARD, type(b.get_native()))

    def test_filepath(self):
        b = Board()
        self.assertEqual("", b.filepath)
        b.filepath = "path/to/board.kicad_mod"
        self.assertEqual("path/to/board.kicad_mod", b.filepath)

    def test_eq(self):
        bp = _pcbnew.BOARD()
        b1 = Board(bp)
        b2 = Board(bp.GetBoard())
        self.assertEqual(b1, b2)

    @unittest.skip("Board.from_editor() seems to return a new BOARD object")
    def test_eq_from_editor(self):
        b1 = Board.from_editor()
        b2 = Board.from_editor()
        self.assertEqual(b1, b2)

    def test_neq(self):
        b1 = Board()
        b2 = Board()
        self.assertNotEqual(b1, b2)

    def test_neq_other_types(self):
        b1 = Board()
        self.assertNotEqual(b1, None)
        self.assertNotEqual(b1, 1)
        self.assertNotEqual(b1, "foo")
