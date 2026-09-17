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
#  Change log:
#    2026-09-05  KSM  Created
#    2026-09-09  KSM  Changed rendering to buffered DC; reduced flickering
#    2026-09-11  KSM  Implemented rules select/change
#    2026-09-17  KSM  Added grid context menu
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
# ******************************************************************************

import wx
from cgol_game_engine import GameEngine
from cgol_context_menu import GridContextMenu
from typing import Callable


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
        self._highlight_cell_color = (0, 255, 0)
        self._grid_color = (128, 128, 128)
        self._is_paused : bool = True
        self._is_grid_visible : bool = True
        self._grid_data = self._engine.grid_data()
        self.__show_message : Callable[[str],None]|None = None
        self.__highlight_cell : tuple[int,int]|None = None

        self._buffer_bitmap = wx.Bitmap(1,1)
        self.w_cell = 0
        self.h_cell = 0

        self._menu = GridContextMenu(self)

        self.SetMinSize(wx.Size(self.w_cell * self.cols, self.h_cell * self.rows))
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size_panel)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click)

        self.SetDoubleBuffered(True)


    def __set_highlight_cell(self, pos:tuple[int,int]|None=None):
        """Set the coordinate of the highlighted cell or clear it

        Args:
            pos: [None]   clear the highlighted cell {default}
                 [tuple]  (row,col) = highlighted cell coordinate
        """
        self.__highlight_cell = pos


    def set_message_handler(self, fnmessage:Callable[[str],None]):
        """Sets the message handler function from the parent

        Args:
            fnmessage: [Callable] function to display status message
        """
        self.__show_message = fnmessage


    def show_message(self, message:str):
        """Generate a transient message in the stauts bar "message" field

        Args:
            message: [str] Message to show. Defaults="" -> clears the field.
            time_ms: [int] Time to display in msec. Default=0 -> use global
        """
        if self.__show_message:
            self.__show_message(message)


    def configure(self, *,
                  color:tuple[int,int,int]|None=None,
                  cell_wh:tuple[int,int]|None=None,
                  size:tuple[int,int]|None=None,
                  highlight:tuple[int,int,int]|None=None,
                  grid:tuple[int,int,int]|None=None):
        """Configure grid-specific settings that cannot be done during construction

        Args:
            color: Live-cell color (R,G,B). Default=None -> do not set color
            cell_wh: Cell width and height (w,h). Default=None -> do not set w, h
            size:  grid size (rows, cols). Default=None -> do not set size
            highlight: Color (R,G,B). Default=None -> do not set highlight
        """
        if color is not None:
            self._live_cell_color = color
        if cell_wh is not None:
            self.w_cell, self.h_cell = cell_wh
        if size is not None:
            self.rows, self.cols = size
            self.SetMinSize(wx.Size(self.w_cell * self.cols, self.h_cell * self.rows))
        if highlight is not None:
            self._highlight_cell_color = highlight
        if grid is not None:
            self._grid_color = grid


    def advance_generation(self) -> int:
        """Advances the game of life one generation

        Returns:
            Number of live cells in the new generation
        """
        live_cells = self._engine.advance_generation()
        self._sync_from_engine()
        self.__render_grid_to_buffer()
        return live_cells


    def redraw_grid(self):
        """Force a redraw of the grid
        """
        self.__render_grid_to_buffer()


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
    def games_names_list(self) -> list[str]:
        """Property: list of preset and loaded games

        Returns:
            Returns a list of names of preset and loaded games
        """
        return self._engine.games_names_list


    @property
    def games_rules_list(self) -> list[str]:
        """Property: list of rules

        Returns:
            List of unique rules of preset and loaded games
        """
        return self._engine.games_rules_list


    @property
    def rules(self) -> str:
        """Property: rules

        Returns:
            [str]   rules in B/S form: ex/ "B3/S23"
        """
        return self._engine.rules


    @rules.setter
    def rules(self, rules:str):
        """Property: rules setter

        Args:
            rules: [str]   rules in B/S form: ex/ "B3/S23"
        """
        self._engine.rules = rules


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
    def is_grid_visible(self) -> bool:
        """Property: is the grid visible

        Returns:
            True if grid visible; False if grid not visible
        """
        return self._is_grid_visible


    @is_grid_visible.setter
    def is_grid_visible(self, visible:bool):
        """Set the grid visibility

        Args:
            visible: True -> grid visible; False -> grid not visible
        """
        self._is_grid_visible = visible


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


    def __render_grid_to_buffer(self):
        """Render the bitmap DC
        """
        # --- Start with a fresh, blank canvas ---
        dc = wx.MemoryDC(self._buffer_bitmap)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        # --- Configure the "alive cell" brush and pen ---
        dc.SetBrush(wx.Brush(wx.Colour(*self._live_cell_color)))
        dc.SetPen(wx.TRANSPARENT_PEN)					  # Removes the 1px cell

        # --- Draw every live cell ---
        for r in range(self.rows):
            for c in range(self.cols):
                if self._grid_data[r,c]:
                    x = c * self.w_cell
                    y = r * self.h_cell
                    dc.DrawRectangle(x, y, self.w_cell, self.h_cell)

        # --- Draw highlight, if any ---
        if self.__highlight_cell is not None:
            dc.SetBrush(wx.Brush(wx.Colour(*self._highlight_cell_color)))
            r, c = self.__highlight_cell
            x = c * self.w_cell
            y = r * self.h_cell
            dc.DrawRectangle(x, y, self.w_cell, self.h_cell)

        # --- Draw the grid, if visible ---
        if self._is_grid_visible:
            info = wx.PenInfo(colour=wx.Colour(*self._grid_color), width=1, style=wx.PENSTYLE_SOLID)
            dc.SetPen(wx.Pen(info))
            nr, nc = self.size()
            x0, x2 = 0, nc*self.w_cell
            y0, y2 = 0, nr*self.h_cell
            for i in range(nr+1):
                y = i * self.h_cell
                p0 = wx.Point(x0, y)
                p2 = wx.Point(x2, y)
                dc.DrawLine(p0, p2)
            for j in range(nc+1):
                x = j * self.w_cell
                p0 = wx.Point(x, y0)
                p2 = wx.Point(x, y2)
                dc.DrawLine(p0, p2)


    def on_paint(self, event:wx.PaintEvent):
        """EVT_PAINT hanndler for the game grid panel; draws the panel

        Args:
            event: [wx.PaintEvent]
        """
        _ = wx.BufferedDC(wx.PaintDC(self), self._buffer_bitmap)
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
                self.__render_grid_to_buffer()
                self.Refresh()

        # --- Allow the event to propagate further if needed ---
        event.Skip()


    def on_right_click(self, event:wx.MouseEvent):
        """EVT_RIGHT_DOWN handler for the panel grid

        Args:
            event: [wx.MouseEvent]
        """
        if self._is_paused:
            pos = event.GetPosition()
            click_col = pos.x // self.w_cell
            click_row = pos.y // self.h_cell

            if not ( 0 <= click_row < self.rows  and 0 <= click_col < self.cols ):
                return

            self.__set_highlight_cell((click_row, click_col))
            self.__render_grid_to_buffer()
            self.Refresh()

            result = self._menu.show_context_menu(pos)

            if result is not None:
                if isinstance(result, int):
                    if result == 0:
                        self._engine.clear()
                        self.show_message("Cleared grid...")
                elif isinstance(result, tuple):
                    # generate an object with head at the grid location
                    label, pattern, head = result
                    head_row, head_col = head
                    pos_at = (click_row - head_row, click_col - head_col)
                    self._engine.add_pattern_at(pattern, pos_at)
                    self.show_message(f"Added {label.lower()}...")

            self.__set_highlight_cell(None)
            self._sync_from_engine()
            self.__render_grid_to_buffer()
            self.Refresh()
        else:
            self.show_message("Pause to access menu...")


    def on_size_panel(self, event:wx.SizeEvent):
        """EVT_SIZE handler

        Args:
            event: [wx.SizeEvent]
        """
        w, h = self.GetClientSize()
        if w>0 and h>0:
            self._buffer_bitmap = wx.Bitmap(w, h)
            self.__render_grid_to_buffer()
        event.Skip()


    def on_erase_background(self, event:wx.Event):
        """EVT_ERASE_BACKGROUND handler

        Catch this event and do nothing. This will eliminate flickering.

        Args:
            event: [wx.Event]  not used
        """
        pass
        # event.Skip()  do not call self.Skip()


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************