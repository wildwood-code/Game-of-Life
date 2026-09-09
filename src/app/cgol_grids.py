# ******************************************************************************
#  Unlicensed. Free for usage without warranty, expressed or implied
#
#  Implementation of Conway's Game of Life
#
#  Filename   : cgol_grids.py
#  Description:
#    This file contains several predefined CGoL games (grids)
#
#    format: ("name", rows, cols, "init-string"),
#    tuple[str, int, int, str]
#
#    "name" is the name of the grid pattern
#    rows, cols specifies the normal grid size, the pattern is centered in the grid
#    "init-string" is the pattern...
#      one text row per pattern row
#      one text column per pattern column
#      use . for dead cells (avoid spaces)
#      use x, *, #, or most other non-space chars for live cells
#
#  Note:
#    retain the given spacing with the """ text field justified to the left margin
#
#  Change log:
#    2026-09-05  KSM  Created
#    2026-09-09  KSM  Updated the comment to include this change log
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
# ******************************************************************************

GRID_GLIDER = (
"Glider", 32, 32, True,
"""\
x.x
.xx
.x.
"""
)

GRID_BEACON = (
"Beacon", 16, 16, True,
"""\
xx..
xx..
..xx
..xx
"""
)

GRID_PENTADECATHLON = (
"Pentadecathlon-15", 48, 48, True,
"""\
xxx
.x.
.x.
xxx
...
xxx
xxx
...
xxx
.x.
.x.
xxx
"""
)

GRID_PULSAR = (
"Pulsar-3", 32, 32, True,
"""\
..xxx...xxx..
.............
x....x.x....x
x....x.x....x
x....x.x....x
..xxx...xxx..
.............
..xxx...xxx..
x....x.x....x
x....x.x....x
x....x.x....x
.............
..xxx...xxx..
"""
)

GRID_LWSS = (
"Spaceship LWSS", 16, 32, True,
"""\
.xxxx
x...x
....x
x..x.
"""
)

GRID_MWSS = (
"Spaceship MWSS", 16, 32, True,
"""\
..x...
x...x.
.....x
x....x
.xxxxx
"""
)

GRID_HWSS = (
"Spaceship HWSS", 16, 32, True,
"""\
.xxxxxx
x.....x
......x
x....x.
..xx...
"""
)

GRID_TOAD = (
"Toad", 16, 16, True,
"""\
.xxx
xxx.
"""
)

GRID_BLINKER = (
"Blinker", 16, 16, True,
"""\
xxx
"""
)

GRID_B_HEPTOMINO = (
"B-heptomino", 80, 80, False,
"""\
x.xx
xxx.
.x..
"""
)

GRID_I_HEPTOMINO = (
"I-heptomino", 80, 80, False,
"""\
..xx
.xx.
.x..
xx..
"""
)

GRID_GOSPER = (
"Gosper's glider gun", 64, 64, False,
"""\
........................x...........
......................x.x...........
............xx......xx............xx
...........x...x....xx............xx
xx........x.....x...xx..............
xx........x...x.xx....x.x...........
..........x.....x.......x...........
...........x...x....................
............xx......................
"""
)

GRID_BLANK_SMALL = (
"Blank grid, small", 16, 16, True,
" "
)

GRID_BLANK_MID = (
"Blank grid, mid", 32, 32, True,
" "
)

GRID_BLANK_LARGE = (
"Blank grid, large", 64, 64, True,
" "
)


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************