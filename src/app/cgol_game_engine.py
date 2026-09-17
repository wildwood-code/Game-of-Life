# ******************************************************************************
#  Unlicensed. Free for usage without warranty, expressed or implied
#
#  Implementation of Conway's Game of Life
#
#  Filename   : cgol_game_engine.py
#  Description:
#    This Python program implements a simple zero-player game known as
#    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
#    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
#
#    This file implements the GameEngine object. The game engine interfaces
#    between the GUI and the core Game object.
#
#  Change log:
#    2026-09-05  KSM  Created
#    2026-09-09  KSM  Changed class Game to newer CGOL_Game
#    2026-09-11  KSM  Implemented rules select/change
#    2026-09-13  KSM  Consolidated redundant rows, cols, name variables
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
# ******************************************************************************

from cgol_class import CGOL_Game
import wx
import os
import numpy as np
import numpy.typing as npt


class GameEngine:
    """The game engine interfaces between the GUI and the Game object
    """

    def __init__(self):
        """GameEngine constructor
        """
        self._game = CGOL_Game()


    @property
    def name(self) -> str:
        """GameEngine property: name

        Returns:
            Name of the game
        """
        return self._game.name


    @property
    def rules(self) -> str:
        """GameEngine property: rules

        Returns:
            [str]   rules in B/S form: ex/ "B3/S23"
        """
        return self._game.rules


    @rules.setter
    def rules(self, rules:str):
        """GameEngine property: rules setter

        Args:
            rules: [str]   rules in B/S form: ex/ "B3/S23"
        """
        self._game.rules = rules


    @property
    def games_names_list(self) -> list[str]:
        """GameEngine property: list of all games

        Returns:
            List of the names of all preset and loaded games
        """
        return self._game.games_names_list


    @property
    def games_rules_list(self) -> list[str]:
        """GameEngine property: list of all unique rule sets

        Returns:
            Set of unique rules of all preset and loaded games
        """
        games = self._game.games_list
        all_rules = { g[4] for g in games }
        return sorted(list(all_rules))


    @property
    def live_cells(self) -> int:
        """GameEngine property: live cell count

        Returns:
            Number of live cells in the grid
        """
        return self._game.live_cells


    def take_snapshot(self) -> str:
        """Take and store a snapshot of the current game

        Returns:
            [str] pattern of the current game
        """
        return self._game.get_snapshot()


    def restore_snapshot(self, snapshot:str) -> bool:
        """Restore a previous game
        """
        return self._game.set_snapshot(snapshot)


    def grid_data(self) -> npt.NDArray[np.bool_]:
        """Get a copy of the actual game grid data (used for double buffering)

        Returns:
            Numpy NPArray of bool grid cells
        """
        return self._game.grid_data()


    def advance_generation(self) -> int:
        """Step to the next generation in the game

        Returns:
            Number of live cells
        """
        return self._game.advance_generation()


    def size(self) -> tuple[int, int]:
        """Get the size of the game grid

        Returns:
            Size as tuple (rows, cols)
        """
        return self._game.size()


    @property
    def is_warp(self) -> bool:
        """Property: warp state for the game

        Returns:
            True=warp; False=disintegrate
        """
        return self._game.is_warp


    @is_warp.setter
    def is_warp(self, warp:bool):
        """Setter: warp state for the game

        Args:
            warp: rue = warp at edges; False = disintegrate at edges
        """
        self._game.is_warp = warp


    def __getitem__(self, key:tuple[int,int]) -> bool:
        """Get the state of a current grid cell

        Args:
            key: tuple (row, col)

        Returns:
            True == live cell; False == dead cell
        """
        return self._game[*key]


    def __setitem__(self, key:tuple[int,int], value:bool):
        """Set the state of a grid cell in the current grid

        Args:
            key: tuple (row, col)
            value: True => live cell; False => dead cell
        """
        self._game[*key] = value


    def load_file(self, parent:wx.Panel) -> bool:
        """Load a game from a file using Open file dialog

        Args:
            parent: parent Panel for the dialog

        Returns:
            True if a file was loaded; False otherwise
        """
        wildcard = "CGOL files (*.cgol)|*.cgol|All files (*.*)|*.*"

        result = False

        with wx.FileDialog(
            parent=parent,
            message="Open file...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_OK:
                filename = fileDialog.GetPath()
                result = self._game.load_file(filename)

        return result


    def load_preset(self, preset:int) -> tuple[int, int, str]:
        """Load/reload a preset game

        Args:
            preset: [int] index to preset in games list

        Returns:
            [tuple] (rows, cols, name)
        """
        self._game.load_preset(preset)
        name = self._game.name
        rows, cols = self._game.size()
        return (rows, cols, name)


    def resize_game(self, size:tuple[int,int]):
        """Resize the game grid without clearing (it will clip edges if shrunk)

        Args:
            rows: Target number of rows
            cols: Target number of columns
        """
        rows, cols = size
        self._game.resize(rows, cols, anchor="x")


    def new_game(self, *, size:tuple[int,int]=(0,0), name:str="") -> tuple[int, int, str]:
        """Create a new, blank game grid

        Args:
            rows: Target number of rows
            cols: Target number of columns
            name: Name of the game. Defaults to "".

        Returns:
            Tuple (rows, cols, name)
        """
        rows, cols = size
        self._game.clear(rows=rows, cols=cols)
        self._game.name = name
        rows, cols = self._game.size()
        return (rows, cols, name)


    def clear(self):
        """Clear the game grid
        """
        self._game.clear()


    def add_pattern_at(self, pattern:str, pos:tuple[int,int]):
        """Add pattern to the game grid at the given location

        Args:
            pattern: [str]  pattern to create
            pos: [int,int]  position at which pattern will be created

        Note:
            upper-left (NW) corner of pattern will be created at the position
        """
        self._game.add_pattern_at(pattern, pos)


    def save_file(self, parent:wx.Panel) -> bool:
        """Save a game to a file using the Save dialog

        Args:
            parent: parent Panel for the dialog

        Returns:
            True if a file was saved; False otherwise
        """
        wildcard = "CGOL files (*.cgol)|*.cgol|All files (*.*)|*.*"
        result = False
        with wx.FileDialog(
            parent=parent,
            message="Save file as...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_OK:
                filename = fileDialog.GetPath()
                result = self._game.save_file(filename)

        return result


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************