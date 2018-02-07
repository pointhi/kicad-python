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

_pcbnew = __import__('pcbnew')  # We need to import the pcbnew module this way, otherwise we try to import us ourself


class Module(object):
    def __init__(self, module=None):
        if module is None:
            module = _pcbnew.MODULE()

        self._obj = module

    def get_native(self):
        # TODO: get_repr, get_native, get_internal, ...?
        return self._obj

    @staticmethod
    def from_editor():
        """Get the current board"""
        return Module(_pcbnew.GetModule())  # TODO: in footprint editor, working?

    @staticmethod
    def from_file(path):
        return Module(_pcbnew.LoadModule(path))  # TODO: working?

    @staticmethod
    def from_source(source):
        pass  # TODO: missing

    def save_file(path):
        pass  # TODO: missing

    def save_in_lib(library_path):
        pass  # TODO: missing
