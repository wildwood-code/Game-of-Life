# ******************************************************************************
#  Unlicensed. Free for usage without warranty, expressed or implied
#
#  Implementation of Conway's Game of Life
#
#  Filename   : cgol_game_grid.py
#  Description:
#    This Python program implements a simple zero-player game known as
#    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
#    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
#
#    This file implements pnlGameGrid, the wx.Panel object that draws and
#    maintains the game grid. It interfaces between the GUI frame and the
#    game engine.
#
#  Created    : 2026-09-05
#  Modified   : 2026-09-05
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
# ******************************************************************************

import wx
from cgol_game_engine import GameEngine


class pnlGameGrid(wx.Panel):

    def __init__(self, parent: wx.Window,
                 id: int = wx.ID_ANY,
                 pos: wx.Point = wx.DefaultPosition,
                 size: wx.Size = wx.DefaultSize,
                 style: int = wx.TAB_TRAVERSAL,
                 name: str = wx.PanelNameStr):
        """pnlGameGrid constructor

        Args:
            parent: Parent wxPython object
            id: ID for the constructed object. Defaults to wx.ID_ANY.
            pos: Position of the object. Defaults to wx.DefaultPosition.
            size: Size of the object. Defaults to wx.DefaultSize.
            style: Style of the object. Defaults to wx.TAB_TRAVERSAL.
            name: Name of the object. Defaults to wx.PanelNameStr.
        """
        super().__init__(parent)

        self.rows = 0
        self.cols = 0
        self._engine = GameEngine()
        self._live_cell_color = (0, 0, 0)
        self._is_paused : bool = True
        self._grid_data = self._engine.grid_data()

        dc = wx.ScreenDC()
        self.w_cell = 0
        self.h_cell = 0

        self.SetMinSize(wx.Size(self.w_cell * self.cols, self.h_cell * self.rows))
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size_panel)


    def configure(self, *,
                  color:tuple[int,int,int]|None=None,
                  cell_wh:tuple[int,int]|None=None,
                  size:tuple[int,int]|None=None):
        """Configure grid-specific settings that cannot be done during construction

        Args:
            color: Live-cell color (R,G,B). Default=None -> do not set color
            cell_wh: Cell width and height (w,h). Default=None -> do not set w, h
        """
        if color is not None:
            self._live_cell_color = color
        if cell_wh is not None:
            self.w_cell, self.h_cell = cell_wh
        if size is not None:
            self.rows, self.cols = size
            self.SetMinSize(wx.Size(self.w_cell * self.cols, self.h_cell * self.rows))


    def advance_generation(self) -> int:
        """Advances the game of life one generation

        Returns:
            Number of live cells in the new generation
        """
        live_cells = self._engine.advance_generation()
        self._sync_from_engine()
        return live_cells


    def load_preset(self, game:int) -> tuple[int, int, str]:
        """Loads a preset game

        Args:
            game: Index to game preset

        Returns:
            (rows, cols, name)
        """
        self._engine.load_preset(game)
        self._is_paused = True
        self.rows, self.cols = self._engine.size()
        self.configure(size=(self.rows, self.cols))
        self._sync_from_engine()
        return (self.rows, self.cols, self._engine.name)


    def new_game(self, *, size:tuple[int,int], name:str="") -> tuple[int, int, str]:
        """Generates a new, blank game of the given size

        Args:
            size: Size of the game grid (rows, cols)
            name: Name to give the new game. Default=""

        Returns:
            (rows, cols, name)
        """
        self.rows, self.cols, name = self._engine.new_game(size=size, name=name)
        self._sync_from_engine()
        return (self.rows, self.cols, name)


    @property
    def games_list(self) -> list[str]:
        """Property: list of preset and loaded games

        Returns:
            Returns a list of names of preset and loaded games
        """
        return self._engine.games_list


    @property
    def is_paused(self) -> bool:
        """Property: check if the game is paused

        Returns:
            True if the game is paused; False if it is running
        """
        return self._is_paused


    @is_paused.setter
    def is_paused(self, paused:bool):
        """Setter: set the paused state of the game

        Args:
            paused: True=pause game; False=run game
        """
        self._is_paused = paused


    @property
    def name_of_game(self) -> str:
        """Property: get the name of the game

        Returns:
            Name of the currently loaded game
        """
        return self._engine.name


    @property
    def live_cells(self) -> int:
        """Property: count of live cells in the game grid

        Returns:
            Number of live cells in the game grid
        """
        return self._engine.live_cells


    def resize_game(self, size:tuple[int,int]):
        """Resize the game grid without clearing the game grid contents

        Args:
            size: (rows, cols)
        """
        self._engine.resize_game(size=size)
        rows, cols = self._engine.size()
        self._sync_from_engine()
        self.configure(size=(rows, cols))


    def size(self) -> tuple[int, int]:
        """Get the size of the game grid

        Returns:
            (rows, cols)
        """
        return (self.rows, self.cols)


    @property
    def is_warp(self) -> bool:
        """Property: warp state for the engine

        Returns:
            True=warp; False=disintegrate
        """
        return self._engine.is_warp


    @is_warp.setter
    def is_warp(self, warp:bool):
        """Setter: warp state for the engine

        Args:
            warp: True=warp; False=disintegrate
        """
        self._engine.is_warp = warp


    def _sync_from_engine(self):
        """Synchronize the display buffer from the game engine
        """
        self._grid_data = self._engine.grid_data()
        self.Refresh() # Queue a screen repaint event


    def load_file(self) -> bool:
        """Open a dialog to load a file to the game engine

        Returns:
            True if a file was loaded; False if it was cancelled or failed
        """
        if self._engine.load_file(self):
            rows, cols = self._engine.size()
            self.configure(size=(rows, cols))
            self._sync_from_engine()
            return True
        return False


    def save_file(self) -> bool:
        """Open a dialog to save a file from the game engine

        Returns:
            True if the file was saved; False if it was cancelled or failed
        """
        return self._engine.save_file(self)


    def take_snapshot(self) -> str:
        """Take and store a snapshot of the current game grid

        Returns:
            [str] pattern of the current grid
        """
        return self._engine.take_snapshot()


    def restore_snapshot(self, snapshot:str) -> bool:
        """Restore the last saved snapshot to the current game grid
        """
        if self._engine.restore_snapshot(snapshot):
            self._sync_from_engine()
            self.Refresh()
            return True
        return False


    def on_paint(self, event:wx.PaintEvent):
        """EVT_PAINT hanndler for the game grid panel; draws the panel

        Args:
            event: [wx.PaintEvent]
        """
        # --- Start with a fresh, blank canvas ---
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        # --- Configure the "alive cell" brush and pen ---
        dc.SetBrush(wx.Brush(wx.Colour(*self._live_cell_color)))
        dc.SetPen(wx.TRANSPARENT_PEN)					  # Removes the 1px cell

        # --- Draw every live cell ---
        for r in range(self.rows):
            for c in range(self.cols):
                if self._grid_data[r,c]: #self._engine[r, c]:
                    x = c * self.w_cell
                    y = r * self.h_cell
                    dc.DrawRectangle(x, y, self.w_cell, self.h_cell)

        event.Skip()


    def do_panel_click(self, event:wx.MouseEvent):
        """Called from the parent frame EVT_LEFT_DOWN event handler

        This method toggles the cell that is clicked

        Args:
            event: [wx.MouseEvent]
        """
        if self._is_paused:
            if self._engine is not None and self._grid_data is not None:
                # --- Get the exact pixel coordinate where the user clicked ---
                pixel_pos = event.GetPosition()
                click_x = pixel_pos.x
                click_y = pixel_pos.y

                # --- Divide by your cell size to get the grid row/column ---
                col = click_x // self.w_cell
                row = click_y // self.h_cell

                # --- Toggle your cell state here ---
                nr, nc = self._engine.size()
                if 0 <= row < nr and 0 <= col < nc:
                    cell = not self._engine[row, col]
                    self._engine[row, col] = cell
                    self._grid_data[row, col] = cell

                # --- Force the panel to refresh/repaint the screen ---
                self.Refresh()

        # --- Allow the event to propagate further if needed ---
        event.Skip()


    def on_size_panel(self, event:wx.SizeEvent):
        """EVT_SIZE handler

        Args:
            event: [wx.SizeEvent]
        """
        event.Skip()


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************