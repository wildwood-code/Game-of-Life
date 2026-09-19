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
#    2026-09-18  KSM  Fixed live cell count after adding structure
#    2026-09-18  KSM  Added ability to load .cgol file passed as argument
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

        self.__rows, self.__cols = 0, 0
        self.__engine = GameEngine()
        self.__live_cell_color = (0, 0, 0)
        self.__highlight_cell_color = (0, 255, 0)
        self.__grid_color = (128, 128, 128)
        self.__is_paused : bool = True
        self.__is_grid_visible : bool = True
        self.__grid_data = self.__engine.grid_data()
        self.__fn_show_message : Callable[[str],None]|None = None
        self.__fn_update_status : Callable[[],None]|None = None
        self.__highlight_cell : tuple[int,int]|None = None

        self.__buffer_bitmap = wx.Bitmap(1,1)
        self.__w_cell, self.__h_cell = 0, 0

        self.__menu = GridContextMenu(self)

        self.SetMinSize(wx.Size(self.__w_cell * self.__cols, self.__h_cell * self.__rows))
        self.Bind(wx.EVT_PAINT, self.__on_paint)
        self.Bind(wx.EVT_SIZE, self.__on_size_panel)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.__on_erase_background)
        self.Bind(wx.EVT_RIGHT_DOWN, self.__on_right_click)
        self.Bind(wx.EVT_LEFT_DOWN, self.__on_panel_click)

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
        self.__fn_show_message = fnmessage


    def set_status_update_handler(self, fnstatus:Callable[[],None]):
        """Sets the status update handler function from the parent

        Args:
            fnstatus: [Callable] function to update status bar
        """
        self.__fn_update_status = fnstatus


    def __show_message(self, message:str):
        """Generate a transient message in the stauts bar "message" field

        Args:
            message: [str] Message to show. Defaults="" -> clears the field.
            time_ms: [int] Time to display in msec. Default=0 -> use global
        """
        if self.__fn_show_message:
            self.__fn_show_message(message)


    def __update_status_bar(self):
        """Update the text on the status bar
        """
        if self.__fn_update_status:
            self.__fn_update_status()


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
            self.__live_cell_color = color
        if cell_wh is not None:
            self.__w_cell, self.__h_cell = cell_wh
        if size is not None:
            self.__rows, self.__cols = size
            self.SetMinSize(wx.Size(self.__w_cell * self.__cols, self.__h_cell * self.__rows))
        if highlight is not None:
            self.__highlight_cell_color = highlight
        if grid is not None:
            self.__grid_color = grid


    def advance_generation(self) -> int:
        """Advances the game of life one generation

        Returns:
            Number of live cells in the new generation
        """
        live_cells = self.__engine.advance_generation()
        self.__sync_from_engine()
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
        self.__engine.load_preset(game)
        self.__is_paused = True
        self.__rows, self.__cols = self.__engine.size()
        self.configure(size=(self.__rows, self.__cols))
        self.__sync_from_engine()
        return (self.__rows, self.__cols, self.__engine.name)


    def new_game(self, *, size:tuple[int,int], name:str="") -> tuple[int, int, str]:
        """Generates a new, blank game of the given size

        Args:
            size: Size of the game grid (rows, cols)
            name: Name to give the new game. Default=""

        Returns:
            (rows, cols, name)
        """
        self.__rows, self.__cols, name = self.__engine.new_game(size=size, name=name)
        self.__sync_from_engine()
        return (self.__rows, self.__cols, name)


    @property
    def games_names_list(self) -> list[str]:
        """Property: list of preset and loaded games

        Returns:
            Returns a list of names of preset and loaded games
        """
        return self.__engine.games_names_list


    @property
    def games_rules_list(self) -> list[str]:
        """Property: list of rules

        Returns:
            List of unique rules of preset and loaded games
        """
        return self.__engine.games_rules_list


    @property
    def rules(self) -> str:
        """Property: rules

        Returns:
            [str]   rules in B/S form: ex/ "B3/S23"
        """
        return self.__engine.rules


    @rules.setter
    def rules(self, rules:str):
        """Property: rules setter

        Args:
            rules: [str]   rules in B/S form: ex/ "B3/S23"
        """
        self.__engine.rules = rules


    @property
    def is_paused(self) -> bool:
        """Property: check if the game is paused

        Returns:
            True if the game is paused; False if it is running
        """
        return self.__is_paused


    @is_paused.setter
    def is_paused(self, paused:bool):
        """Setter: set the paused state of the game

        Args:
            paused: True=pause game; False=run game
        """
        self.__is_paused = paused


    @property
    def name_of_game(self) -> str:
        """Property: get the name of the game

        Returns:
            Name of the currently loaded game
        """
        return self.__engine.name


    @property
    def live_cells(self) -> int:
        """Property: count of live cells in the game grid

        Returns:
            Number of live cells in the game grid
        """
        return self.__engine.live_cells


    def resize_game(self, size:tuple[int,int]):
        """Resize the game grid without clearing the game grid contents

        Args:
            size: (rows, cols)
        """
        self.__engine.resize_game(size=size)
        rows, cols = self.__engine.size()
        self.__sync_from_engine()
        self.configure(size=(rows, cols))


    def size(self) -> tuple[int, int]:
        """Get the size of the game grid

        Returns:
            (rows, cols)
        """
        return (self.__rows, self.__cols)


    @property
    def is_grid_visible(self) -> bool:
        """Property: is the grid visible

        Returns:
            True if grid visible; False if grid not visible
        """
        return self.__is_grid_visible


    @is_grid_visible.setter
    def is_grid_visible(self, visible:bool):
        """Set the grid visibility

        Args:
            visible: True -> grid visible; False -> grid not visible
        """
        self.__is_grid_visible = visible


    @property
    def is_warp(self) -> bool:
        """Property: warp state for the engine

        Returns:
            True=warp; False=disintegrate
        """
        return self.__engine.is_warp


    @is_warp.setter
    def is_warp(self, warp:bool):
        """Setter: warp state for the engine

        Args:
            warp: True=warp; False=disintegrate
        """
        self.__engine.is_warp = warp


    def __sync_from_engine(self):
        """Synchronize the display buffer from the game engine
        """
        self.__grid_data = self.__engine.grid_data()
        self.Refresh() # Queue a screen repaint event


    def load_file(self, filename:str|None=None) -> bool:
        """Open a dialog to load a file to the game engine

        Returns:
            True if a file was loaded; False if it was cancelled or failed
        """
        if self.__engine.load_file(self, filename):
            rows, cols = self.__engine.size()
            self.configure(size=(rows, cols))
            self.__sync_from_engine()
            return True
        return False


    def save_file(self) -> bool:
        """Open a dialog to save a file from the game engine

        Returns:
            True if the file was saved; False if it was cancelled or failed
        """
        return self.__engine.save_file(self)


    def take_snapshot(self) -> str:
        """Take and store a snapshot of the current game grid

        Returns:
            [str] pattern of the current grid
        """
        return self.__engine.take_snapshot()


    def restore_snapshot(self, snapshot:str) -> bool:
        """Restore the last saved snapshot to the current game grid
        """
        if self.__engine.restore_snapshot(snapshot):
            self.__sync_from_engine()
            self.Refresh()
            return True
        return False


    def __render_grid_to_buffer(self):
        """Render the bitmap DC
        """
        # --- Start with a fresh, blank canvas ---
        dc = wx.MemoryDC(self.__buffer_bitmap)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        # --- Configure the "alive cell" brush and pen ---
        dc.SetBrush(wx.Brush(wx.Colour(*self.__live_cell_color)))
        dc.SetPen(wx.TRANSPARENT_PEN)					  # Removes the 1px cell

        # --- Draw every live cell ---
        for r in range(self.__rows):
            for c in range(self.__cols):
                if self.__grid_data[r,c]:
                    x = c * self.__w_cell
                    y = r * self.__h_cell
                    dc.DrawRectangle(x, y, self.__w_cell, self.__h_cell)

        # --- Draw highlight, if any ---
        if self.__highlight_cell is not None:
            dc.SetBrush(wx.Brush(wx.Colour(*self.__highlight_cell_color)))
            r, c = self.__highlight_cell
            x = c * self.__w_cell
            y = r * self.__h_cell
            dc.DrawRectangle(x, y, self.__w_cell, self.__h_cell)

        # --- Draw the grid, if visible ---
        if self.__is_grid_visible:
            info = wx.PenInfo(colour=wx.Colour(*self.__grid_color), width=1, style=wx.PENSTYLE_SOLID)
            dc.SetPen(wx.Pen(info))
            nr, nc = self.size()
            x0, x2 = 0, nc*self.__w_cell
            y0, y2 = 0, nr*self.__h_cell
            for i in range(nr+1):
                y = i * self.__h_cell
                p0 = wx.Point(x0, y)
                p2 = wx.Point(x2, y)
                dc.DrawLine(p0, p2)
            for j in range(nc+1):
                x = j * self.__w_cell
                p0 = wx.Point(x, y0)
                p2 = wx.Point(x, y2)
                dc.DrawLine(p0, p2)


    def __on_paint(self, event:wx.PaintEvent):
        """EVT_PAINT hanndler for the game grid panel; draws the panel

        Args:
            event: [wx.PaintEvent]
        """
        _ = wx.BufferedDC(wx.PaintDC(self), self.__buffer_bitmap)
        event.Skip()


    def __on_panel_click(self, event:wx.MouseEvent):
        """Called from the parent frame EVT_LEFT_DOWN event handler

        This method toggles the cell that is clicked

        Args:
            event: [wx.MouseEvent]
        """
        if self.__is_paused:
            if self.__engine is not None and self.__grid_data is not None:
                # --- Get the exact pixel coordinate where the user clicked ---
                pixel_pos = event.GetPosition()
                click_x = pixel_pos.x
                click_y = pixel_pos.y

                # --- Divide by your cell size to get the grid row/column ---
                col = click_x // self.__w_cell
                row = click_y // self.__h_cell

                # --- Toggle your cell state here ---
                nr, nc = self.__engine.size()
                if 0 <= row < nr and 0 <= col < nc:
                    cell = not self.__engine[row, col]
                    self.__engine[row, col] = cell
                    self.__grid_data[row, col] = cell

                # --- Force the panel to refresh/repaint the screen ---
                self.__render_grid_to_buffer()
                self.__update_status_bar()
                self.Refresh()
        else:
            self.__show_message("Pause to edit grid...")

        # --- Allow the event to propagate further if needed ---
        event.Skip()


    def __on_right_click(self, event:wx.MouseEvent):
        """EVT_RIGHT_DOWN handler for the panel grid

        Args:
            event: [wx.MouseEvent]
        """
        if self.__is_paused:
            pos = event.GetPosition()
            click_col = pos.x // self.__w_cell
            click_row = pos.y // self.__h_cell

            if not ( 0 <= click_row < self.__rows  and 0 <= click_col < self.__cols ):
                return

            self.__set_highlight_cell((click_row, click_col))
            self.__render_grid_to_buffer()
            self.Refresh()

            result = self.__menu.show_context_menu(pos)

            if result is not None:
                if isinstance(result, int):
                    if result == 0:
                        self.__engine.clear()
                        self.__show_message("Cleared grid...")
                elif isinstance(result, tuple):
                    # generate an object with head at the grid location
                    label, pattern, head = result
                    head_row, head_col = head
                    pos_at = (click_row - head_row, click_col - head_col)
                    self.__engine.add_pattern_at(pattern, pos_at)
                    self.__show_message(f"Added {label.lower()}...")

            self.__set_highlight_cell(None)
            self.__sync_from_engine()
            self.__render_grid_to_buffer()
            self.__update_status_bar()
            self.Refresh()
        else:
            self.__show_message("Pause to access menu...")


    def __on_size_panel(self, event:wx.SizeEvent):
        """EVT_SIZE handler

        Args:
            event: [wx.SizeEvent]
        """
        w, h = self.GetClientSize()
        if w>0 and h>0:
            self.__buffer_bitmap = wx.Bitmap(w, h)
            self.__render_grid_to_buffer()
        event.Skip()


    def __on_erase_background(self, event:wx.Event):
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