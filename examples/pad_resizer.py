#!/usr/bin/env python

from __future__ import print_function

import argparse

from kicad.pcbnew import Board

from kicad.util.point import Point2D


def resize_pads(board, minimal_drill, minimal_annular_ring):
    for module in board.modules:
        print("Resize pads of: {}".format(module))
        for pad in module.pads:
            assert pad.drill_size.x == pad.drill_size.y  # we assume round holes
            
            if pad.drill_size.x == 0:
                print("* skip SMD pad")
                continue
            
            if pad.drill_size.x < minimal_drill:
                new_size = Point2D([minimal_drill, minimal_drill])
                size_difference = new_size - pad.drill_size

                print("* modify drill size from {} to {}".format(pad.drill_size, new_size))
                pad.size += size_difference  # modify annular ring
                pad.drill_size = new_size  # set to minimal size

            annular_size = pad.size - pad.drill_size
            if annular_size.x < minimal_annular_ring:
                new_size = pad.size  # currently required because kicad-python cannot do pad.size.x = ...
                new_size.x = pad.drill_size.x + minimal_annular_ring

                print("* modify size (x) from {} to {}".format(pad.size, new_size))
                pad.size = new_size

            if annular_size.y < minimal_annular_ring:
                new_size = pad.size  # currently required because kicad-python cannot do pad.size.y = ...
                new_size.y = pad.drill_size.y + minimal_annular_ring

                print("* modify size (y) from {} to {}".format(pad.size, new_size))
                pad.size = new_size


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('board', help='board file to list elements', action='store')
    parser.add_argument('minimal_drill', help='minimal drill size', type=float, default=0., action='store')
    parser.add_argument('minimal_copper', help='minimal copper size to solder', type=float, default=0., action='store')

    args = parser.parse_args()

    board = Board.from_file(args.board)

    resize_pads(board, args.minimal_drill, args.minimal_copper*2)

    print()
    save_path = board.filepath + ".new"  # save with new name
    print("save board in: {}".format(save_path))
    board.to_file(save_path)
