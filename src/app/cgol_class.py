# ******************************************************************************
#  Unlicensed. Free for usage without warranty, expressed or implied
#
#  Implementation of Conway's Game of Life
#
#  Filename   : cgol_class.py
#  Description:
#    This Python program implements a simple zero-player game known as
#    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
#    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
#
#    My implementation takes several parts:
#      Grid class : implements a resizeable grid of bool
#      Game class : implements game rules
#
#    My grid warps at the boundaries. Patterns like Gosper's Glider Gun will
#    eventually collide and cease working correctly.
#
#  Created    : 2026-09-05
#  Modified   : 2026-09-05
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
# ******************************************************************************

import numpy as np
import numpy.typing as npt
from static_init import static_init
import re
from typing import Literal
import cgol_grids as grids
from pathlib import Path
import io


@static_init
class Grid:

    @classmethod
    def static_init(cls):
        # characters for displaying grid
        # use ASCII characters as these will be used for file I/O
        cls.LIVE_CELL = "#"  # filled cell: used when cell state is True
        cls.DEAD_CELL = "."  # center dot: used when cell state is False
        cls.DEAD_SET  = [" ", "."]  # chars recognized as "dead"

        # regular expressions
        cls.RE_PARSE_GRID = re.compile(r"^(.+)$", re.MULTILINE)


    def __init__(self, obj:"Grid|str|None"=None, *, rows:int=0, cols:int=0):
        """Grid constructor

        Args:
            obj:  [Grid] Initialization object. See Notes.
            obj:  [str]  String used to initialize grid. See Notes
            obj:  [None] Create an empty grid {default}
            rows: [int]  Number of grid rows {default 0 => auto}
            cols: [int]  Number of grid columns {default 0 => auto}

        Raises:
            Exception: raised if the initialization string is invalid

        Notes:
            The initialization object is used to initialize the grid upon
            construction. It may be another Grid object, in which case the
            grid is copied. It may be a string, with one row per line. Use "."
            to denote a False/dead grid cell and "x" to denote a True/live grid
            cell. The default is an empty grid.

            If a size is not given, the size is determined by the number of rows
            and cols in the initialization object.

            If a size is given, rows and cols, then the constructed grid is
            resized to that given size, with any initialized grid centered.
        """
        # first, create an empty grid
        self._nr = 0
        self._nc = 0
        self._data = np.zeros((0,0), dtype=bool)

        # next, precreate an initialized grid from a Grid or string
        if isinstance(obj, Grid):
            self._nr = obj._nr
            self._nc = obj._nc
            self._data = obj._data.copy()

        elif isinstance(obj, str):
            # lines are separated by newlines
            # space, period, or cdot are "dead"
            # everything else is "live"
            success = False
            m = Grid.RE_PARSE_GRID.findall(obj)
            while m is not None: # if-loop with break out
                nr = len(m)
                if not nr > 0: break
                nc = len(m[0])
                if not nc > 0: break
                self._nr = nr
                self._nc = nc
                self._data = np.zeros((nr, nc), dtype=bool)
                dead_set = Grid.DEAD_SET
                for i in range(nr):
                    row = m[i]
                    if not len(row) == nc: break
                    for j in range(nc):
                        if not row[j] in dead_set:
                            self._data[i,j] = True
                success = True
                break

            if not success:
                raise Exception("Invalid init string")

        # finally, adjust the size
        if rows != self._nr or cols != self._nr:
            self.resize(rows=rows, cols=cols, anchor="ctr")


    def __bool__(self) -> bool:
        """Grid test: is it non-zero-dimension?

        Returns:
            False if the grid is 0x0 dimension; True otherwise
        """
        return self._nr > 0 and self._nc > 0


    def data_copy(self) -> npt.NDArray[np.bool_]:
        """Get a copy of the raw Numpy bool array

        Returns:
            Copy of raw Numpy bool array
        """
        return self._data.copy()


    def clear(self):
        """Clear the grid: make all cells False/dead
        """
        self._data.fill(False)


    def clone(self) -> "Grid":
        """Clone the grid: make a copy of itself

        Returns:
            Returns a new Grid object that is a copy of this one.
        """
        my_clone = Grid(self)
        return my_clone


    def size(self) -> tuple[int,int]:
        """Grid dimensions: recalls the size (rows, cols) of the grid as a tuple

        Returns:
            Tuple (rows, cols)
        """
        return (self._nr, self._nc)


    @property
    def live_count(self) -> int:
        """Grid property: number of True/live grid cells

        Returns:
            Number of True/live grid cells
        """
        live = 0
        for i in range(self._nr):
            for j in range(self._nc):
                if self._data[i, j]: live += 1
        return live


    @property
    def cell_count(self) -> int:
        """Grid property: number of cells in the grid

        Returns:
            Number of cells in the grid, including True/live and False/dead
        """
        return self._nr * self._nc


    @property
    def rows(self) -> int:
        """Grid property: number of rows in the grid

        Returns:
            Number of rows in the grid
        """
        return self._nr


    @property
    def cols(self) -> int:
        """Grid property: number of columns in the grid

        Returns:
            Number of columns in the grid
        """
        return self._nc


    def resize(self, rows:int, cols:int, *, anchor:Literal["ctr", "nw", "n", "ne", "w", "e", "sw", "s", "se"]="nw"):
        """Resize the Grid object

        Args:
            rows:   [int] Target number of rows {default 0}
            cols:   [int] Target number of cols {default 0}
                          0 => don't change rows/cols; + => target rows/cols
            anchor: Anchor position {default "nw"}
                    ["nw", "n", "ne", "w", "ctr", "e", "sw", "s", "se"]
        """

        if rows > 0:
            my_rows, my_cols = self.size()
            rows_t = 0  # number of top rows to add or subtract
            rows_b = 0  # number of bottom rows to add or subtract
            add_rows = rows - my_rows

            match anchor:
                case "ctr" | "w" | "e":
                    # divide equally (favor bottom if odd)
                    rows_t = int(add_rows/2)
                    rows_b = add_rows - rows_t

                case "nw" | "n" | "ne":
                    # add/subtract at bottom
                    rows_b = add_rows

                case "sw" | "s" | "se":
                    # add/subtract at top
                    rows_t = add_rows

            if add_rows > 0:
                data = np.vstack((np.zeros((rows_t, my_cols), dtype=bool), self._data, np.zeros((rows_b, my_cols), dtype=bool)))
                self._data = data
                self._nr = rows

            elif add_rows < 0:
                rows_delete = np.r_[0:-rows_t, my_rows+rows_b:my_rows]
                data = np.delete(self._data, rows_delete, axis=0)
                self._data = data
                self._nr = rows

        if cols > 0:
            my_rows, my_cols = self.size()
            cols_l = 0  # number of left cols to add or subtract
            cols_r = 0  # number of right cols to add or subtract
            add_cols = cols - my_cols

            match anchor:
                case "ctr" | "n" | "s":
                    # divide equally (favor right)
                    cols_l = int(add_cols/2)
                    cols_r = add_cols - cols_l

                case "nw" | "w" | "sw":
                    # add/subtract at right
                    cols_r = add_cols

                case "ne" | "e" | "se":
                    # add/subtract at left
                    cols_l = add_cols

            if add_cols > 0:
                data = np.hstack((np.zeros((my_rows, cols_l), dtype=bool), self._data, np.zeros((my_rows, cols_r), dtype=bool)), dtype=bool)
                self._data = data
                self._nc = cols

            elif add_cols < 0:
                cols_delete = np.r_[0:-cols_l, my_cols+cols_r:my_cols]
                data = np.delete(self._data, cols_delete, axis=1)
                self._data = data
                self._nc = cols


    def _coerce(self, pos:tuple[int,int]) -> tuple[int,int]:
        """Coerce the given grid position (r,c) into one within the warped grid

        Args:
            pos: [tuple] Grid position: (r, c)

        Returns:
            [tuple] Coerced grid position: (r, c)
                    (-1, -1) for a 0x0 grid
        """
        r, c = pos
        r = r % self._nr if self._nr != 0 else -1
        c = c % self._nc if self._nc != 0 else -1
        return (r, c)


    def __getitem__(self, pos:tuple[int,int]) -> bool:
        """Grid indexing: obj[r, c]

        Args:
            pos: [tuple] Position in the grid as a tuple (r, c)

        Returns:
            Grid state True/False at the given position
        """
        r, c = self._coerce(pos)
        return self._data[r, c]


    def __setitem__(self, pos:tuple[int,int], value:bool):
        """Grid indexing: obj[r, c] = value

        Args:
            pos:   [tuple] Position in the grid: (r, c)
            value: [bool] Grid state to set the given position
        """
        r, c = self._coerce(pos)
        self._data[r, c] = value


    def __repr__(self) -> str:
        """Grid representation (partial)

        Returns:
            Displays the grid representation partially. By partially, the size
            is shown and the number of live cells, but not the grid data.
        """
        n_live = self.live_count
        return f"Grid(rows={self._nr}, cols={self._nc}, live_cells={n_live})"


    def __str__(self) -> str:
        """Grid data as a string

        Returns:
            Returns a string with newlines splitting rows. The number of chars
            on each row is the number of columns. The chars used to represent
            live and dead cells is specified in the Grid static variables.
        """
        c_live = Grid.LIVE_CELL
        c_dead = Grid.DEAD_CELL
        grid = ""
        for i in range(self._nr):
            row = ""
            for j in range(self._nc):
                e = c_live if self[i,j] else c_dead
                row = row + e
            grid = grid + row
            if i < self._nr-1:
                grid = grid + "\n"
        return grid


@static_init
class Game:

    @classmethod
    def static_init(cls):
        cls.GAMES : list[tuple[str, int, int, bool, str]] = \
        [   # format: ("name", rows, cols, "init-string")
            grids.GRID_GLIDER,
            grids.GRID_BEACON,
            grids.GRID_TOAD,
            grids.GRID_BLINKER,
            grids.GRID_PENTADECATHLON,
            grids.GRID_B_HEPTOMINO,
            grids.GRID_I_HEPTOMINO,
            grids.GRID_PULSAR,
            grids.GRID_LWSS,
            grids.GRID_MWSS,
            grids.GRID_HWSS,
            grids.GRID_GOSPER,
            grids.GRID_BLANK_SMALL,
            grids.GRID_BLANK_MID,
            grids.GRID_BLANK_LARGE
        ]


    def __init__(self, obj:"Game|None"=None):
        """Game constructor

        Args:
            obj:  {optional} Game object. Make self a copy if obj is passed.
            rows: Number of grid rows. Defaults to 0.
            cols: Number of grid cols. Defaults to 0.
            init: Initialization string
        """

        if isinstance(obj, Game):
            # make a copy of the Game object that was supplied
            self._name = obj._name
            self._is_warp = obj._is_warp
            self._grid = [Grid(obj._grid[0]), Grid(obj._grid[1])]
            self._rows, self._cols = obj._rows, obj._cols
            self._idx = obj._idx
            self._games_list : list[tuple[str, int, int, bool, str]] = obj._games_list.copy()
            self._live_cells = obj._live_cells

        else:
            # initialize to empty Game
            self._name = ""
            self._is_warp = True
            self._grid = [Grid(), Grid()]
            self._rows, self._cols = 0, 0
            self._idx = 0
            self._games_list : list[tuple[str, int, int, bool, str]] = Game.GAMES.copy()
            self._live_cells = 0


    def load_pattern(self, pattern:str, *, name:str, rows:int=0, cols:int=0, is_warp:bool=True):
        """Load a game from a pattern

        Args:
            pattern: [str] pattern for game grid
            name:    [str] name to give game
            rows:    [int] number of rows; defaults to 0 -> auto
            cols:    [int] number of columns; defaults to 0 -> auto
            is_warp: [bool] True = warp at edge; False = disintegrate at edge
        """
        if pattern:
            # game grid from pattern
            self._grid = [ Grid(pattern, rows=rows, cols=cols),
                           Grid(rows=rows, cols=cols) ]
        else:
            # empty game grid
            self._grid = [ Grid(rows=rows, cols=cols),
                           Grid(rows=rows, cols=cols) ]

        self._name = name.strip()
        self._rows, self._cols = self._grid[0].size()
        self._idx = 0  # points at the active grid
        self._live_cells = self._grid[0].live_count
        self._is_warp = is_warp
        self._register_game()


    def load_preset(self, preset:int) -> tuple[int, int, str]:
        """Load/reload a preset game

        Args:
            preset: [int] index to preset in games list

        Returns:
            [tuple] (rows, cols, name)
        """
        self._name = ""

        Ngames = len(self._games_list)
        igame = preset % Ngames
        my_game_spec = self._games_list[igame]
        n_rows = my_game_spec[1]
        n_cols = my_game_spec[2]
        self._name = my_game_spec[0].strip()
        self._is_warp = my_game_spec[3]
        self._grid = [Grid(my_game_spec[4], rows=n_rows, cols=n_cols),
                    Grid(rows=n_rows, cols=n_cols)]
        self._live_cells = self._grid[0].live_count
        self._rows, self._cols = self._grid[0].size()
        self._idx = 0  # points at the active grid

        return (self._rows, self._cols, self._name)


    @staticmethod
    def __read_from_open_file(file: io.TextIOWrapper|io.StringIO) -> tuple[str, int, int, bool, str]|None:
        """Read a game descriptor from an open file

        Args:
            file: open file or StringIO object

        Returns:
            game descriptor (name, rows, cols, is_warp, pattern)
        """
        result = None
        is_success = True
        try:
            name = file.readline()
            rows_cols = file.readline()
            if m := re.match(r"\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*(True|False)\s*$", rows_cols):
                # new format: rows, cols, True/False
                rows = int(m.group(1))
                cols = int(m.group(2))
                is_warp = not (m.group(3)=="False")
            elif m := re.match(r"\s*([0-9]+)\s*,\s*([0-9]+)\s*$", rows_cols):
                # old format: rows, cols
                rows = int(m.group(1))
                cols = int(m.group(2))
                is_warp = True
            else:
                is_success = False
        except:
            is_success = False
        if is_success:
            my_pattern = ""
            try:
                for r in range(rows):
                    my_row = file.readline()
                    my_pattern += my_row + "\n"
            except:
                is_success = False
        if is_success:
            result = (name, rows, cols, is_warp, my_pattern)
        return result


    def load_file(self, filename:str) -> bool:
        """Load a game from a file

        Args:
            filename: [str] filename of the file to be loaded

        Returns:
            True if file was successfully loaded; False otherwise
        """
        try:
            with open(filename, 'r') as file:
                load_result = Game.__read_from_open_file(file)
                if load_result:
                    name, rows, cols, is_warp, my_pattern = load_result
                try:
                    self.load_pattern(pattern=my_pattern, name=name, rows=rows, cols=cols, is_warp=is_warp)
                except:
                    raise ValueError()
        except IOError:
            return False
        except ValueError:
            return False
        return True


    def set_snapshot(self, snapshot:str) -> bool:
        """Sets the game grid from the given snapshot

        Args:
            snapshot: [str] essentially the text format in a .cgol file

        Returns:
            True if successful; False otherwise

        Notes:
            The snapshot rows and cols must match exactly. The purpose of this
            function is to support taking/restoring snapshots of the grid.
        """
        result = False
        with io.StringIO(snapshot) as file_like:
            if load_result := Game.__read_from_open_file(file_like):
                _, rows, cols, _, pattern = load_result
                if rows==self._rows and cols==self._cols and pattern:
                    # if we made it this far, pattern should be valid
                    self._grid[self._idx] = Grid(pattern, rows=rows, cols=cols)
                    result = True
        return result


    @staticmethod
    def __write_to_open_file(file: io.TextIOWrapper|io.StringIO,
                             desc:tuple[str,int,int,bool,str]) -> bool:
        """Write a game descriptor to an open file

        Args:
            file: open file or StringIO object
            desc: game descriptor (name, rows, cols, is_warp, pattern)

        Returns:
            True if successful; False otherwise
        """
        result = True
        name, rows, cols, is_warp, pattern = desc
        try:
            file.write(f"{name}\n")
            str_warp = "True" if is_warp else "False"
            file.write(f"{rows}, {cols}, {str_warp}\n")
            file.write(pattern)
        except:
            result = False

        return result


    def get_snapshot(self) -> str:
        result = ""
        with io.StringIO() as file_like:
            pattern = str(self)
            game_set = (self._name, self._rows, self._cols, self._is_warp, pattern)
            if Game.__write_to_open_file(file_like, game_set):
                result = file_like.getvalue()
        return result


    def save_file(self, filename:str, *, name:str="") -> bool:
        """_summary_

        Args:
            filename: [str] filename of the file to be saved
            name:     [str] optional name to assign to game {default "" => use filename stem}

        Returns:
            True if file was successfully saved; False otherwise
        """
        file_path = Path(filename)
        try:
            with open(filename, 'w') as file:
                if name:
                    self._name = name.strip()
                else:
                    self._name = file_path.stem.strip()
                pattern = str(self)
                game_set = (self._name, self._rows, self._cols, self._is_warp, pattern)
                if Game.__write_to_open_file(file, game_set):
                    self._register_game()
                else:
                    return False
        except IOError:
            return False
        return True


    def _register_game(self):
        """Register the current game as a game in the games list (overwrite
        if a game with the same name exists)
        """
        name = self._name
        if any(t[0]==name for t in self._games_list):
            # overwrite the matching games_list entry
            for idx in range(len(self._games_list)):
                if self._games_list[idx][0] == name:
                    entry = (name, self._rows, self._cols, self._is_warp, str(self))
                    self._games_list[idx] = entry
                    break
        else:
            # add a new games_list entry at the end
            my_pattern = str(self)
            self._games_list.append((name, self._rows, self._cols, self._is_warp, my_pattern))


    @property
    def games_list(self) -> list[str]:
        """Property: get a list of game names

        Returns:
            A list of the names of all of the preset and loaded games
        """
        return [ t[0] for t in self._games_list]


    def grid_copy(self) -> npt.NDArray[np.bool_]:
        """Get a copy of the actual grid data of the active grid

        Returns:
            Copy of NDArray[bool] grid array
        """
        return self._grid[self._idx].data_copy()


    def size(self) -> tuple[int,int]:
        """Game grid dimensions: recalls the size (rows, cols) of the grid as a tuple

        Returns:
            Tuple (rows, cols)
        """
        return self._grid[self._idx].size()


    @property
    def rows(self) -> int:
        """Property: number of rows

        Returns:
            Number of rows in the grid
        """
        return self._rows


    @property
    def cols(self) -> int:
        """Property: number of columns

        Returns:
            Number of columns in the grid
        """
        return self._cols


    @property
    def name(self) -> str:
        """Property: game name

        Returns:
            Name of the game
        """
        return self._name


    @property
    def is_warp(self) -> bool:
        """Property: is_warp

        Returns:
            True = warp at edges; False = disintegrate at edges
        """
        return self._is_warp


    @is_warp.setter
    def is_warp(self, warp):
        """Setter: is_warp

        Args:
            warp: rue = warp at edges; False = disintegrate at edges
        """
        self._is_warp = warp


    def clear(self, rows:int=0, cols:int=0):
        """Clear the grid and optionally resize

        Args:
            rows: rows dimension. Default=0 -> do not resize rows
            cols: columns dimension. Default=0 -> do not resize cols
        """
        self._grid[0].clear()
        self._grid[1].clear()
        if rows>0 and cols>0:
            self._grid[0].resize(rows=rows, cols=cols)
            self._grid[1].resize(rows=rows, cols=cols)
        self._idx = 0
        self._live_cells = 0


    def resize(self, rows:int, cols:int, *, anchor:Literal["ctr", "nw", "n", "ne", "w", "e", "sw", "s", "se"]="nw"):
        """Resize the grid in the Game object

        Args:
            rows:   [int] Target number of rows {default 0}
            cols:   [int] Target number of cols {default 0}
                          0 => don't change rows/cols; + => target rows/cols
            anchor: Anchor position {default "nw"}
                    ["nw", "n", "ne", "w", "ctr", "e", "sw", "s", "se"]
        """
        self._grid[0].resize(rows=rows, cols=cols, anchor=anchor)
        self._grid[1].resize(rows=rows, cols=cols, anchor=anchor)
        self._live_cells = self._grid[self._idx].live_count


    @staticmethod
    def __rules_warp(grid_now:Grid, grid_next:Grid) -> int:
        """Execute rules for grid with warp at edges

        Args:
            grid_now: grid in the current generation
            grid_next: grid calculated for the new generation

        Returns:
            live cell count for the new generation
        """
        live_cells : int = 0
        nr, nc = grid_next.size()
        for i in range(nr):
            for j in range(nc):
                # get our current state of life
                life = grid_now[i, j]

                # count the neighbors
                neighbors = 0
                for k in range(-1, 2): # -1, 0, 1
                    if grid_now[i+k, j-1]: neighbors += 1
                    if grid_now[i+k, j+1]: neighbors += 1
                if grid_now[i-1,j]: neighbors += 1
                if grid_now[i+1,j]: neighbors += 1

                # rules:
                if life and neighbors < 2:
                    # live cell with < 2 neighbors dies by underpopulation
                    life = False
                elif life and neighbors > 3:
                    # live cell with > 3 neighbors dies by overpopulation
                    life = False
                elif not life and neighbors == 3:
                    # dead cell with 3 neighbors is born by reproduction
                    life = True
                else:
                    # life goes on
                    pass

                if life: live_cells += 1
                grid_next[i, j] = life

        return live_cells


    @staticmethod
    def __disintegrate_at_edges(grid:Grid, live_cells:int) -> int:
        """Disintegrate structures at edges: Breadth-First Search (BFS) algorithm

        Args:
            grid_now: grid in the current generation
            live_cells: current live cell count

        Returns:
            live cell count after disintegration
        """
        n_rows, n_cols = grid.size()
        visited = set()
        to_kill = set()

        # identify all live cells sitting at the borders
        border_cells = []
        for r in range(n_rows):
            if grid[r,0]: border_cells.append((r,0))
            if grid[r,n_cols-1]: border_cells.append((r,n_cols-1))
        for c in range(n_cols):
            if grid[0,c]: border_cells.append((0,c))
            if grid[n_rows-1,c]: border_cells.append((n_rows-1,c))

        # flood fill to find the entire structure
        for start_r, start_c in border_cells:
            start_coord = (start_r, start_c)
            if start_coord in visited:
                continue

            # standard BFS queue
            queue = [start_coord]
            visited.add(start_coord)

            while queue:
                r, c = queue.pop(0)
                to_kill.add((r, c))
                # check all 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        key = (nr,nc)
                        # if neighbor is in bounds, alive, and not yet visited
                        if 0 <= nr < n_rows and 0 <= nc < n_cols:
                            if grid[key] and key not in visited:
                                visited.add(key)
                                queue.append(key)

            # disintegrate the entire structure
            for key in to_kill:
                grid[key] = False
                live_cells -= 1

        return live_cells


    def step(self) -> int:
        """Generate the next evolution step in the Game of Life

        Returns:
            Number of live cells
        """
        idx_now = self._idx
        idx_next = 0 if idx_now else 1
        grid_now = self._grid[idx_now]
        grid_next = self._grid[idx_next]
        grid_next.clear()
        live_cells = self.__rules_warp(grid_now, grid_next)
        if not self._is_warp:
            live_cells = self.__disintegrate_at_edges(grid_next, live_cells)
        self._idx = idx_next
        self._live_cells = live_cells
        return live_cells


    @property
    def live_cells(self) -> int:
        """Property: live cell count

        Returns:
            Returns the number of live cells
        """
        return self._live_cells


    def __str__(self) -> str:
        """String representation of the current grid

        Returns:
            String representing the current grid. Newlines separate rows.
        """
        return str(self._grid[self._idx])


    def __repr__(self) -> str:
        """Representation of the Game object

        Returns:
            "Game(rows=#, cols=#, live_cells=#)"
        """
        nr, nc = self._grid[self._idx].size()
        n_live = self._grid[self._idx].live_count
        return f"Game(rows={nr}, cols={nc}, live_cells={n_live})"


    def __getitem__(self, key:tuple[int,int]) -> bool:
        """Gets the state of a cell in the current grid

        Args:
            key: [tuple] (row, col)

        Returns:
            True == live cell; False == dead cell
        """
        return self._grid[self._idx][key]


    def __setitem__(self, key:tuple[int,int], value:bool):
        """Sets the state of a cell in the current grid

        Args:
            key:   [tuple] (row, col)
            value: [bool] True => live cell; False => dead cell
        """
        cell = self._grid[self._idx][key]
        if cell != value:
            if value:
                self._live_cells += 1
            else:
                self._live_cells -= 1
        self._grid[self._idx][key] = value


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************