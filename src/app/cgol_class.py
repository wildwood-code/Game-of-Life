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
#  Change log:
#    2026-09-05  KSM  Created
#    2026-09-09  KSM  Replaced "indexed grid" with single-grid
#                     Replaced Grid with CellArray
#                     Derive CGOL_Game from protocol class Game
#                     Added use of "B/S" rules specifier (defaults to B3/S23)
#    2026-09-11  KSM  Implemented rules select/change
#    2026-09-13  KSM  Consolidated redundant rows, cols, name variables
#                     Added new games
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
from CellArray import CellArray, ResizeAnchor
from Game_protocol import Game, Rules, RuleSpec, CellArraySize, Designator, GamesList, GameSpec

@static_init
class CGOL_Game(Game):

    @classmethod
    def static_init(cls):
        cls.DEFAULT_RULES = "B3/S23"
        cls.GAMES : list[GameSpec] = \
        [   # format: ("name", rows, cols, is_warp, rules, "init-string")
            grids.GRID_GLIDER,
            grids.GRID_BEACON,
            grids.GRID_TOAD,
            grids.GRID_BLINKER,
            grids.GRID_PENTADECATHLON,
            grids.GRID_B_HEPTOMINO,
            grids.GRID_I_HEPTOMINO,
            grids.GRID_R_PENTOMINO,
            grids.GRID_PULSAR,
            grids.GRID_DIEHARD,
            grids.GRID_ACORN,
            grids.GRID_LWSS,
            grids.GRID_MWSS,
            grids.GRID_HWSS,
            grids.GRID_GOSPER,
            grids.GRID_SIMKIN,
            grids.GRID_BLANK_SMALL,
            grids.GRID_BLANK_MID,
            grids.GRID_BLANK_LARGE
        ]


    def __init__(self, obj:"CGOL_Game|None"=None):
        """Game constructor

        Args:
            obj:  {optional} Game object. Make self a copy if obj is passed.
        """

        my_rules = Game._decode_rules(CGOL_Game.DEFAULT_RULES)

        if isinstance(obj, CGOL_Game):
            # make a copy of the Game object that was supplied
            self._name = obj._name
            self._is_warp = obj._is_warp
            self._grid = CellArray(obj._grid, dtype=bool)
            self._games_list : list[GameSpec] = obj._games_list.copy()
            self._live_cells = obj._live_cells
            self._rule_spec : RuleSpec = my_rules

        else:
            # initialize to empty Game
            self._name = ""
            self._is_warp = True
            self._grid = CellArray(dtype=bool)
            self._games_list : list[GameSpec] = CGOL_Game.GAMES.copy()
            self._live_cells = 0
            self._rule_spec : RuleSpec = my_rules


    @property
    def rules(self) -> Rules:
        return Game._encode_rules(self._rule_spec)


    @rules.setter
    def rules(self, rules:Rules):
        self._rule_spec : RuleSpec = Game._decode_rules(rules)


    def new_game(self, *, size:CellArraySize, name:str="", is_warp:bool=True) -> Designator:
        """Create a new, blank game grid

        Args:
            size:    [tuple] (rows, cols)
            name:    [str]   Name of the game. Defaults to "".
            is_warp: [bool]  True=warp edge; False=non-warp edge

        Returns:
            [tuple] (rows, cols, name)
        """
        self._name = name
        self._is_warp = is_warp
        self._size = size
        self._live_cells = 0
        self._grid : CellArray[bool] = CellArray[bool](size=self._size, dtype=bool)


    def load_pattern(self, pattern:str, *, name:str, rows:int=0, cols:int=0, is_warp:bool=True, rules:str="B3/S23"):
        """Load a game from a pattern

        Args:
            pattern: [str] pattern for game grid
            name:    [str] name to give game
            rows:    [int] number of rows; defaults to 0 -> auto
            cols:    [int] number of columns; defaults to 0 -> auto
            is_warp: [bool] True = warp at edge; False = disintegrate at edge
            rules:   [str] rules spec in B/S form; default = "B3/S23"
        """
        if pattern:
            # game grid from pattern
            self._grid = CellArray(pattern, size=(rows, cols))
        else:
            # empty game grid
            self._grid = CellArray(size=(rows, cols))

        self._name = name.strip()
        self._live_cells = self._grid.live_count
        self._is_warp = is_warp
        self._rule_spec = Game._decode_rules(rules)
        self._register_game()


    def load_preset(self, preset:int) -> tuple[int, int, str]:
        """Load/reload a preset game

        Args:
            preset: [int] index to preset in games list

        Returns:
            [tuple] (rows, cols, name)
        """
        Ngames = len(self._games_list)
        igame = preset % Ngames
        my_game_spec = self._games_list[igame]
        n_rows = my_game_spec[1]
        n_cols = my_game_spec[2]
        self._name = my_game_spec[0].strip()
        self._is_warp = my_game_spec[3]
        self._rule_spec = Game._decode_rules(my_game_spec[4])
        self._grid = CellArray(my_game_spec[5], size=(n_rows, n_cols))
        self._live_cells = self._grid.live_count
        rows, cols = self._grid.size
        return (rows, cols, self._name)


    @staticmethod
    def __read_from_open_file(file: io.TextIOWrapper|io.StringIO) -> GameSpec|None:
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
            if m := re.match(r"\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*(True|False)\s*,\s*(B[1-8]+\/S[0-8]+)\s*$", rows_cols):
                # 1.3 format: rows, cols, True/False
                rows = int(m.group(1))
                cols = int(m.group(2))
                is_warp = not (m.group(3)=="False")
                rules = m.group(4)
            elif m := re.match(r"\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*(True|False)\s*$", rows_cols):
                # 1.0 format: rows, cols, True/False
                rows = int(m.group(1))
                cols = int(m.group(2))
                is_warp = not (m.group(3)=="False")
                rules = "B3/S23"
            elif m := re.match(r"\s*([0-9]+)\s*,\s*([0-9]+)\s*$", rows_cols):
                # 0.0 format: rows, cols
                rows = int(m.group(1))
                cols = int(m.group(2))
                is_warp = True
                rules = "B3/S23"
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
            result = (name, rows, cols, is_warp, rules, my_pattern)
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
                if load_result := CGOL_Game.__read_from_open_file(file):
                    name, rows, cols, is_warp, rules, my_pattern = load_result
                try:
                    self.load_pattern(pattern=my_pattern, name=name, rows=rows, cols=cols, is_warp=is_warp, rules=rules)
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
            if read_snap := CGOL_Game.__read_from_open_file(file_like):
                _, snap_rows, snap_cols, _, _, snap_pattern = read_snap
                rows, cols = self._grid.size
                if snap_rows==rows and snap_cols==cols and snap_pattern:
                    # if we made it this far, pattern should be valid
                    self._grid = CellArray(snap_pattern, size=(snap_rows, snap_cols))
                    result = True
        return result


    @staticmethod
    def __write_to_open_file(file: io.TextIOWrapper|io.StringIO,
                             desc:GameSpec) -> bool:
        """Write a game descriptor to an open file

        Args:
            file: open file or StringIO object
            desc: game descriptor (name, rows, cols, is_warp, pattern)

        Returns:
            True if successful; False otherwise
        """
        result = True
        name, rows, cols, is_warp, rules, pattern = desc
        try:
            file.write(f"{name}\n")
            str_warp = "True" if is_warp else "False"
            file.write(f"{rows}, {cols}, {str_warp}, {rules}\n")
            file.write(pattern)
        except:
            result = False

        return result


    def get_snapshot(self) -> str:
        """Take a snapshot of the current grid

        Returns:
            [str]  representing a snapshot of the current grid
        """
        result = ""
        with io.StringIO() as file_like:
            rows, cols = self._grid.size
            game_set =  \
            (
                self._name,
                rows,
                cols,
                self._is_warp,
                Game._encode_rules(self._rule_spec),
                str(self)
            )
            if CGOL_Game.__write_to_open_file(file_like, game_set):
                result = file_like.getvalue()
        return result


    def save_file(self, filename:str, *, name:str="") -> bool:
        """Saves the game as a .cgol file

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
                rules = Game._encode_rules(self._rule_spec)
                rows, cols = self._grid.size
                game_set = (self._name, rows, cols, self._is_warp, rules, pattern)
                if CGOL_Game.__write_to_open_file(file, game_set):
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
        my_pattern = str(self)
        my_rules = Game._encode_rules(self._rule_spec)
        rows, cols = self._grid.size
        if any(t[0]==name for t in self._games_list):
            # overwrite the matching games_list entry
            for idx in range(len(self._games_list)):
                if self._games_list[idx][0] == name:
                    entry = (name, rows, cols, self._is_warp, my_rules, my_pattern)
                    self._games_list[idx] = entry
                    break
        else:
            # add a new games_list entry at the end
            self._games_list.append((name, rows, cols, self._is_warp, my_rules, my_pattern))


    @property
    def designator(self) -> Designator:
        """<property> Returns a designator of the game size and name

        Returns:
            [tuple]  (rows, cols, name)
        """
        return (*self._size, self._name)


    @property
    def games_list(self) -> GamesList:
        """<property> get a list of games

        Returns:
            A list of the preset and loaded games
        """
        return self._games_list


    @property
    def games_names_list(self) -> list[str]:
        """Property: get a list of game names

        Returns:
            A list of the names of all of the preset and loaded games
        """
        return [ t[0] for t in self._games_list]


    def grid_data(self) -> npt.NDArray:
        """Get a copy of the actual grid data of the game

        Returns:
            [NDArray]  numpy array of grid data
        """
        return self._grid.data_copy()


    def size(self) -> tuple[int,int]:
        """Game grid dimensions: recalls the size (rows, cols) of the grid as a tuple

        Returns:
            Tuple (rows, cols)
        """
        return self._grid.size


    @property
    def rows(self) -> int:
        """Property: number of rows

        Returns:
            Number of rows in the grid
        """
        return self._grid.rows


    @property
    def cols(self) -> int:
        """Property: number of columns

        Returns:
            Number of columns in the grid
        """
        return self._grid.cols


    @property
    def name(self) -> str:
        """Property: game name

        Returns:
            Name of the game
        """
        return self._name


    @name.setter
    def name(self, name:str):
        """Property setter: game name

        Args:
            name: [str]  Name of the game
        """
        if isinstance(name, str):
            self._name = name


    @property
    def is_warp(self) -> bool:
        """Property: is_warp

        Returns:
            True = warp at edges; False = disintegrate at edges
        """
        return self._is_warp


    @is_warp.setter
    def is_warp(self, warp:bool):
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
        self._grid.clear()
        if rows>0 and cols>0:
            self._grid.resize(size=(rows, cols))
        self._live_cells = 0


    def add_pattern_at(self, pattern:str, pos:tuple[int,int]):
        """Add pattern to the grid at the given location

        Args:
            pattern: [str]  pattern to create
            pos: [int,int]  position at which pattern will be created

        Note:
            upper-left (NW) corner of pattern will be created at the position
        """
        r, c = pos
        array = CellArray(pattern)
        nr, nc = array.size
        my_rows, my_cols = self.size()

        for i in range(nr):
            for j in range(nc):
                ir = r + i
                jc = c + j
                if not self._is_warp:
                    # if not warped, skip anything beyond our boundary
                    if not (0 <= ir < my_rows and 0 <= jc < my_cols):
                        continue

                old_cell = self._grid[ir,jc]
                new_cell = array[i,j]
                if new_cell != old_cell:
                    self._live_cells += 1 if new_cell else -1
                self._grid[ir,jc] = new_cell


    def resize(self, rows:int, cols:int, *, anchor:ResizeAnchor="nw"):
        """Resize the grid in the Game object

        Args:
            rows:   [int] Target number of rows {default 0}
            cols:   [int] Target number of cols {default 0}
                          0 => don't change rows/cols; + => target rows/cols
            anchor: Anchor position {default "nw"}
                    ["nw", "n", "ne", "w", "ctr", "e", "sw", "s", "se"]
        """
        self._grid.resize(size=(rows, cols), anchor=anchor)
        self._live_cells = self._grid.live_count


    @staticmethod
    def __rules_warp(grid_now:CellArray, grid_next:CellArray, rules:RuleSpec) -> int:
        """Execute rules for grid with warp at edges

        Args:
            grid_now: grid in the current generation
            grid_next: grid calculated for the new generation

        Returns:
            live cell count for the new generation
        """
        live_cells : int = 0
        nr, nc = grid_next.size
        set_born, set_survive = rules
        for i in range(nr):
            for j in range(nc):
                # get our current state of life
                life_now = grid_now[i, j]

                # count the neighbors
                live_neighbors = 0
                for k in range(-1, 2): # -1, 0, 1
                    if grid_now[i+k, j-1]: live_neighbors += 1
                    if grid_now[i+k, j+1]: live_neighbors += 1
                if grid_now[i-1,j]: live_neighbors += 1
                if grid_now[i+1,j]: live_neighbors += 1

                # rules
                if life_now and live_neighbors not in set_survive:
                    # living cell does not survive
                    life_next = False
                elif not life_now and live_neighbors in set_born:
                    # dead cell is born
                    life_next = True
                else:
                    # life goes on
                    life_next = life_now

                if life_now: live_cells += 1
                grid_next[i, j] = life_next

        return live_cells


    @staticmethod
    def __disintegrate_at_edges(grid:CellArray, live_cells:int) -> int:
        """Disintegrate structures at edges: Breadth-First Search (BFS) algorithm

        Args:
            grid_now: grid in the current generation
            live_cells: current live cell count

        Returns:
            live cell count after disintegration
        """
        n_rows, n_cols = grid.size
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


    def advance_generation(self) -> int:
        """Generate the next evolution step in the Game of Life

        Returns:
            Number of live cells
        """
        grid_now = self._grid
        grid_next = CellArray(size=(grid_now.rows, grid_now.cols))
        grid_next.clear()
        live_cells = self.__rules_warp(grid_now, grid_next, self._rule_spec)
        if not self._is_warp:
            live_cells = self.__disintegrate_at_edges(grid_next, live_cells)
        self._grid = grid_next
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
        return str(self._grid)


    def __repr__(self) -> str:
        """Representation of the Game object

        Returns:
            "Game(rows=#, cols=#, live_cells=#)"
        """
        nr, nc = self._grid.size
        n_live = self._grid.live_count
        return f"Game(rows={nr}, cols={nc}, live_cells={n_live})"


    def __getitem__(self, key:tuple[int,int]) -> bool:
        """Gets the state of a cell in the current grid

        Args:
            key: [tuple] (row, col)

        Returns:
            True == live cell; False == dead cell
        """
        return self._grid[key]


    def __setitem__(self, key:tuple[int,int], value:bool):
        """Sets the state of a cell in the current grid

        Args:
            key:   [tuple] (row, col)
            value: [bool] True => live cell; False => dead cell
        """
        cell = self._grid[key]
        if cell != value:
            if value:
                self._live_cells += 1
            else:
                self._live_cells -= 1
        self._grid[key] = value


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************