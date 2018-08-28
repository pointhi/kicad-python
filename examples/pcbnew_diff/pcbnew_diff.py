#!/usr/bin/env python2

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

import argparse
import math

from kicad.pcbnew import Board, Layer
from kicad.primitives import PolygonSet

# Dependencies required for plotting
import numpy
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection


def create_polyset_from_item(board_item):
    """Create PolygonSet from a BoardItem"""
    p = PolygonSet()

    # @see: https://github.com/twlostow/kicad-dev/blob/tom-polygon-gen/qa/polygon_generator/test_polygon_generator.cpp
    segsPerCircle = 64
    correctionFactor = 1.0 / math.cos(math.pi / segsPerCircle)
    # TODO: method not exported in kicad-python by now, which means we need to access it native
    board_item.get_native().TransformShapeWithClearanceToPolygon(p.get_native(), 1, segsPerCircle, correctionFactor)

    return p


def create_polysets_per_net(board, layer):
    """Create PolgonSet for specific layer seperated per net"""
    nets = {}

    def add_polyset(net, polyset):
        if net not in nets:
            nets[net] = []
        nets[net].append(polyset)

    for track in board.tracks:
        if layer not in track.layers:
            continue
        add_polyset(track.net, create_polyset_from_item(track))

    for via in board.vias:
        if layer not in via.layers:
            continue
        add_polyset(via.net, create_polyset_from_item(via))

    for zone in board.zones:
        if layer not in zone.layers:
            continue
        add_polyset(zone.net, create_polyset_from_item(zone))

    for module in board.modules:
        for pad in module.pads:
            if layer not in pad.layers:
                continue
            add_polyset(pad.net, create_polyset_from_item(pad))

    # TODO: drawings

    return nets


def merge_polysets(polysets):
    """Merge multiple PolygonSet into one PolygonSet"""
    p = PolygonSet()

    for ps in polysets:
        p.union(ps)

    return p


def unify_polysets(nets):
    """Merge multiple PolygonSet per Net into one PolygonSet and remove holes"""
    merged_nets = {}
    for net in nets.keys():
        print("unify polyset for net: \"{}\" with {} subpolygons".format(net.name, len(nets[net])))
        merged_nets[net] = merge_polysets(nets[net])
        merged_nets[net].fracture()  # TODO: only for plotting required

    return merged_nets


def patch_collection_from_nets(merged_nets):
    """create matplotlib Polygons for PatchCollection"""
    patches = []
    for net in merged_nets.keys():
        for poly in merged_nets[net]:
            assert len(poly.holes) == 0  # because of fracture() no holes are present
            polygon = Polygon(poly.outline, True)
            patches.append(polygon)

    return patches


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('old_board', help='old board file as original board', action='store')
    # parser.add_argument('new_board', help='new board file to compare to', action='store')  # TODO: implement

    parser.add_argument('--layer', help='layer which should be diffed', action='store', default='F.Cu')

    args = parser.parse_args()

    old_board = Board.from_file(args.old_board)

    layer = Layer.from_name(args.layer)

    # Create Polygons for boards
    nets = create_polysets_per_net(old_board, layer)
    merged_nets = unify_polysets(nets)

    # Start Plotting code
    fig, ax = plt.subplots()

    numpy.random.seed(0)  # same colors always
    colors = 100 * numpy.random.random(len(merged_nets))
    patches = patch_collection_from_nets(merged_nets)
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    p.set_array(colors)

    ax.add_collection(p)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()
    ax.autoscale()

    plt.show()
