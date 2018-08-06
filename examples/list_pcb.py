#!/usr/bin/env python

from __future__ import print_function

import argparse

from kicad.pcbnew import Board
from kicad.pcbnew import Text


def list_pcb(board):
    print()
    print("LIST VIAS:")
    for via in board.vias:
        print(" * Via:   {} - {}/{}".format(via.position, via.drill, via.width))

    print()
    print("LIST TRACKS:")
    for track in board.tracks:
        print(" * Track: {} to {}, width {}".format(track.start, track.end, track.width))

    print()
    print("LIST DRAWINGS:")
    for drawing in board.drawings:
        if type(drawing) is Text:
            print("* Text:    '{}' at {}".format(drawing.text, drawing.position))
        else:
            print("* Drawing: {}".format(drawing))

    print()
    print("LIST MODULES:")
    for module in board.modules:
        print("* Module: {} at {}".format(module.reference, module.position))

    print()
    print("LIST ZONES:")
    for zone in board.zones:
        print("* Zone: '{}' with priority {}".format(zone.net.name, zone.priority))


# reimplementation of pcbnew/python/examples/listPcb.py script using our abstraction layer
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('board', help='board file to list elements', action='store')

    args = parser.parse_args()

    board = Board.from_file(args.board)

    list_pcb(board)
