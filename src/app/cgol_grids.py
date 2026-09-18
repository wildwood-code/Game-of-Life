# ******************************************************************************
#  Unlicensed. Free for usage without warranty, expressed or implied
#
#  Implementation of Conway's Game of Life
#
#  Filename   : cgol_grids.py
#  Description:
#    This file contains several predefined CGoL games (grids)
#
#    format: ("name", rows, cols, is_warp, rules, "init-string"),
#    tuple[str, int, int, bool, str, str]
#
#    "name" is the name of the grid pattern
#    rows, cols specifies the normal grid size, the pattern is centered in the grid
#    is_warp = True if warp-edges; False if non-warp edges
#    rules in B/S format (ex/ standard CGoL is B3/S23)
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
#    2026-09-11  KSM  Implemented rules select/change (new data field)
#    2026-09-13  KSM  Added new games: Acorn, Diehard, R-pentomino, Siskin
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
# ******************************************************************************

GRID_GLIDER = (
"Glider", 32, 32, True, "B3/S23",
"""\
x.x
.xx
.x.
"""
)

GRID_BEACON = (
"Beacon", 16, 16, True, "B3/S23",
"""\
xx..
xx..
..xx
..xx
"""
)

GRID_PENTADECATHLON = (
"Pentadecathlon-15", 48, 48, True, "B3/S23",
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
"Pulsar-3", 32, 32, True, "B3/S23",
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
"Spaceship LWSS", 16, 32, True, "B3/S23",
"""\
.xxxx
x...x
....x
x..x.
"""
)

GRID_MWSS = (
"Spaceship MWSS", 16, 32, True, "B3/S23",
"""\
..x...
x...x.
.....x
x....x
.xxxxx
"""
)

GRID_HWSS = (
"Spaceship HWSS", 16, 32, True, "B3/S23",
"""\
.xxxxxx
x.....x
......x
x....x.
..xx...
"""
)

GRID_TOAD = (
"Toad", 16, 16, True, "B3/S23",
"""\
.xxx
xxx.
"""
)

GRID_BLINKER = (
"Blinker", 16, 16, True, "B3/S23",
"""\
xxx
"""
)

GRID_B_HEPTOMINO = (
"B-heptomino", 80, 80, False, "B3/S23",
"""\
x.xx
xxx.
.x..
"""
)

GRID_I_HEPTOMINO = (
"I-heptomino", 80, 80, False, "B3/S23",
"""\
..xx
.xx.
.x..
xx..
"""
)

GRID_R_PENTOMINO = (
"R-pentomino", 120, 120, True, "B3/S23",
"""\
.xx
xx.
.x.
"""
)

GRID_DIEHARD = (
"Diehard", 48, 48, True, "B3/S23",
"""\
......x.
xx......
.x...xxx
"""
)

GRID_ACORN = (
"Acorn", 80, 80, True, "B3/S23",
"""\
.x.....
...x...
xx..xxx
"""
)

GRID_GOSPER = (
"Gosper glider gun", 64, 64, False, "B3/S23",
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

GRID_SIMKIN = (
"Simkin glider gun", 80, 80, False, "B3/S23",
"""\
xx.....xx........................
xx.....xx........................
.................................
....xx...........................
....xx...........................
.................................
.................................
.................................
.................................
......................xx.xx......
.....................x.....x.....
.....................x......x..xx
.....................xxx...x...xx
..........................x......
.................................
.................................
.................................
....................xx...........
....................x............
.....................xxx.........
.......................x.........
"""
)

GRID_BLANK_SMALL = (
"Blank grid, small", 16, 16, True, "B3/S23",
""
)

GRID_BLANK_MID = (
"Blank grid, mid", 32, 32, True, "B3/S23",
""
)

GRID_BLANK_LARGE = (
"Blank grid, large", 64, 64, True, "B3/S23",
""
)


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************