# ******************************************************************************
#  Unlicensed. Free for usage without warranty, expressed or implied
#
#  Implementation of Conway's Game of Life
#
#  Filename   : game_of_life.py
#  Description:
#    This Python program implements a simple zero-player game known as
#    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
#    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
#
#    This file is the primary app entry point and implements the CGOL object,
#    based upon wxPython wx.Frame. To run this application:
#
#      py game_of_life.py
#
#    The GUI is designed using wxFormBuilder and generated as wxPython code.
#
#  Package dependencies (other than built-in Python packages):
#    wxPython
#    numpy
#
#  Execute the command:
#    py -m pip install numpy wxPython
#  to install the required Python packages
#
#  Created    : 2026-09-05
#  Modified   : 2026-09-05
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
# ******************************************************************************

import os
import sys
import wx
import wx.adv
import math
from static_init import static_init
from enum import IntEnum


SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SRC_DIR not in sys.path:
	sys.path.insert(0, SRC_DIR)

from ui.generated_ui import frmMain, dlgGetDims
import assets.images as images


@static_init
class CGOL(frmMain):

    @classmethod
    def static_init(cls):
        cls.VERSION = "1.0"
        cls.INITIAL_GAME_IDX = 0
        cls.BACKGROUND_COLOR = (240, 240, 240)  # backgnd (red, green, blue)
        cls.LIVE_CELL_COLOR  = (0, 0, 0)        # live cell (red, green, blue)
        cls.CELL_WH          = (12, 12)         # initial cell width, height pixels
        cls.TIMER_MIN_MS:float = 20.0
        cls.TIMER_MAX_MS:float = 200.0
        cls.SLIDER_MAX:int     = 100    # maximum value of slider (DO NOT CHANGE)
        cls.SLIDER_CHG:int     = 10     # amount to change slider with click
        cls.SLIDER_INI:int     = 50     # initial slider value
        cls.COMBO_ACTION_ITEMS = [ "(New game)",  "(Load game)", "(Save game)" ]
        cls.MESSAGE_DISPLAY_MS = 2000   # time to display message on status bar


    class STATUS:
        N_FIELDS : int = 4
        FIELD_WIDTHS : list[int] = [80, 120, 120, -1]
        class IDX(IntEnum):
            FIELD_STATE = 0             # game state: running/paused
            FIELD_LIVE = 1              # number of live cells
            FIELD_GRID = 2              # grid size
            FIELD_MESSAGE = 3           # message field


    def __init__(self, parent):
        """CGOL constructor

        Args:
            parent: Parent object or None if no parent
        """
        super().__init__(parent)

        # --- catch the wxPython lifecycle trap in on_size() ---
        self.is_initialized = False

        # --- Game settings ---
        self.is_paused = True
        self.is_warp = True

        # --- Begin form initialization ---
        self.tbarMain.Realize()
        self.Layout()

        # --- Setup the game engine and grid ---
        self.pnlGrid.configure(color=CGOL.LIVE_CELL_COLOR, cell_wh=CGOL.CELL_WH)
        self.pnlGrid.load_preset(CGOL.INITIAL_GAME_IDX)
        self.live_cells = self.pnlGrid.live_cells
        self.rows, self.cols = self.pnlGrid.size()

        # --- Load all images ---
        self.IMAGE_PLAY         = images.imgPlay
        self.IMAGE_PAUSE        = images.imgPause
        self.IMAGE_STEP         = images.imgStep
        self.IMAGE_FASTER       = images.imgFaster
        self.IMAGE_SLOWER       = images.imgSlower
        self.IMAGE_TAKE_SNAP    = images.imgTakeSnap
        self.IMAGE_RESTORE_SNAP = images.imgRestoreSnap
        self.IMAGE_ABOUT        = images.imgAbout

        # --- Get tool IDs ---
        self.TOOL_ID_PLAY    = self.toolPlay.GetId()
        self.TOOL_ID_STEP    = self.toolStep.GetId()
        self.TOOL_ID_SLOW    = self.toolSlower.GetId()
        self.TOOL_ID_FAST    = self.toolFaster.GetId()
        self.TOOL_ID_TAKE    = self.toolTakeSnap.GetId()
        self.TOOL_ID_RESTORE = self.toolRestoreSnap.GetId()
        self.TOOL_ID_ABOUT   = self.toolAbout.GetId()

        # --- Set initial images on all tools ---
        tbar = self.tbarMain
        CGOL.set_tool_image(tbar, self.TOOL_ID_STEP,    self.IMAGE_STEP)
        CGOL.set_tool_image(tbar, self.TOOL_ID_SLOW,    self.IMAGE_SLOWER)
        CGOL.set_tool_image(tbar, self.TOOL_ID_FAST,    self.IMAGE_FASTER)
        CGOL.set_tool_image(tbar, self.TOOL_ID_TAKE,    self.IMAGE_TAKE_SNAP)
        CGOL.set_tool_image(tbar, self.TOOL_ID_RESTORE, self.IMAGE_RESTORE_SNAP)
        CGOL.set_tool_image(tbar, self.TOOL_ID_ABOUT,   self.IMAGE_ABOUT)
        self.update_toolbar()

        # --- Configure game selector combo box ---
        games_list = self.pnlGrid.games_list
        self.cmbGame.Set(CGOL.COMBO_ACTION_ITEMS + games_list)
        self.cmbGame.SetSelection(len(CGOL.COMBO_ACTION_ITEMS) + CGOL.INITIAL_GAME_IDX)

        # --- Set warp status ---
        self.chkWarpEdge.SetValue(self.is_warp)

        # --- Setup game speed slider ---
        self.sldSpeed.SetRange(0, CGOL.SLIDER_MAX)
        self.sldSpeed.SetValue(CGOL.SLIDER_INI)

        # --- Setup status bar ---
        self.stabStatusBar.SetFieldsCount(CGOL.STATUS.N_FIELDS)
        self.stabStatusBar.SetStatusWidths(CGOL.STATUS.FIELD_WIDTHS)
        self.update_status_bar()
        self.SetStatusBarPane(-1)
        self.timer_message : wx.CallLater|None = None
        self.show_message("")

        # --- Setup key bindings and accelerator table ---
        self.ID_TOGGLE_PLAY = wx.NewIdRef()
        self.ID_ADVANCE_GEN = wx.NewIdRef()
        self.ID_TAKE_SNAP   = wx.NewIdRef()
        self.ID_RESTORE_SNAP = wx.NewIdRef()
        self.ID_TIMER_FASTER = wx.NewIdRef()
        self.ID_TIMER_SLOWER = wx.NewIdRef()
        self.ID_ABOUT = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.on_click_play, id=self.ID_TOGGLE_PLAY)
        self.Bind(wx.EVT_MENU, self.on_click_step, id=self.ID_ADVANCE_GEN)
        self.Bind(wx.EVT_MENU, self.on_take_snap, id=self.ID_TAKE_SNAP)
        self.Bind(wx.EVT_MENU, self.on_restore_snap, id=self.ID_RESTORE_SNAP)
        self.Bind(wx.EVT_MENU, self.on_click_fast, id=self.ID_TIMER_FASTER)
        self.Bind(wx.EVT_MENU, self.on_click_slow, id=self.ID_TIMER_SLOWER)
        self.Bind(wx.EVT_MENU, self.on_click_about, id=self.ID_ABOUT)
        accel_entries = [
            wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_SPACE, self.ID_TOGGLE_PLAY),
            wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord('a'), self.ID_ADVANCE_GEN),
            wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord('t'), self.ID_TAKE_SNAP),
            wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord('r'), self.ID_RESTORE_SNAP),
            wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord('.'), self.ID_TIMER_FASTER),
            wx.AcceleratorEntry(wx.ACCEL_SHIFT,  ord('.'), self.ID_TIMER_FASTER),
            wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord(','), self.ID_TIMER_SLOWER),
            wx.AcceleratorEntry(wx.ACCEL_SHIFT,  ord(','), self.ID_TIMER_SLOWER),
            wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F1, self.ID_ABOUT)
        ]
        accel_table = wx.AcceleratorTable(accel_entries)
        self.SetAcceleratorTable(accel_table)

        # setup and enable the game timer
        self.is_reset_timer = False
        self.timer_period_ms = CGOL.get_timer_ms(CGOL.SLIDER_INI)
        self.tmrGame.Start(self.timer_period_ms)

        self.is_initialized = True


    def show_message(self, message:str="", time_ms:int=0):
        """Generate a transient message in the stauts bar "message" field

        Args:
            message: [str] Message to show. Defaults="" -> clears the field.
            time_ms: [int] Time to display in msec. Default=0 -> use global
        """
        if self.timer_message is not None and self.timer_message.IsRunning():
            # first, kill any existing message
            self.timer_message.Stop()

        self.GetStatusBar().SetStatusText(message, CGOL.STATUS.IDX.FIELD_MESSAGE)

        if message:
            # set a new timer to kill the message
            if time_ms == 0: time_ms = CGOL.MESSAGE_DISPLAY_MS
            self.timer_message = wx.CallLater(time_ms, self.GetStatusBar().SetStatusText, "", CGOL.STATUS.IDX.FIELD_MESSAGE)


    @staticmethod
    def set_tool_image(toolbar:wx.ToolBar, tool_id:int, image:images.PyEmbeddedImage):
        """Set the image for the given tool in a toolbar

        Args:
            toolbar: target toolbar
            tool_id: ID of the target tool on the toolbar
            image:   PyEmbeddedImage object
        """
        bitmap = wx.BitmapBundle.FromBitmap(image.GetBitmap())
        toolbar.SetToolNormalBitmap(tool_id, bitmap)


    @staticmethod
    def get_timer_ms(slider:int) -> int:
        """Map the slider into a timer interval in milliseconds with a lin-log scale

        Args:
            slider: [int] Slider position:

        Returns:
            _description_
        """
        T_MIN = CGOL.TIMER_MIN_MS
        T_MAX = CGOL.TIMER_MAX_MS
        R_TMR = T_MAX/T_MIN
        return int( T_MIN * R_TMR ** ((CGOL.SLIDER_MAX - slider)/CGOL.SLIDER_MAX))


    def update_toolbar(self):
        """Set images for run/pause and enabled state of step buttons
        """
        if self.is_paused:
            CGOL.set_tool_image(self.tbarMain, self.TOOL_ID_PLAY, self.IMAGE_PLAY)
            self.toolStep.Enable(True)
        else:
            CGOL.set_tool_image(self.tbarMain, self.TOOL_ID_PLAY, self.IMAGE_PAUSE)
            self.toolStep.Enable(False)

        self.tbarMain.Realize()


    def update_status_bar(self):
        # Paused/running field
        if self.is_paused:
            self.stabStatusBar.SetStatusText("Paused", CGOL.STATUS.IDX.FIELD_STATE)
        else:
            self.stabStatusBar.SetStatusText("Running", CGOL.STATUS.IDX.FIELD_STATE)

        # Live cell count field
        self.stabStatusBar.SetStatusText(f"Live cells: {self.live_cells}", CGOL.STATUS.IDX.FIELD_LIVE)

        # Grid size field (clickable)
        self.stabStatusBar.SetStatusText(f"{self.rows} x {self.cols}", CGOL.STATUS.IDX.FIELD_GRID)


    def on_panel_click(self, event:wx.MouseEvent):
        """EVT_LEFT_DOWN event handler: intercepts clicks in the game panel

        It then passes the event to the panel and refreshes the live cell count
        afterward.

        Args:
            event: [wx.MouseEvent]
        """
        self.pnlGrid.do_panel_click(event)
        self.live_cells = self.pnlGrid.live_cells
        self.update_status_bar()
        event.Skip()


    def on_timer_tick(self, event:wx.TimerEvent):
        """EVT_TIMER event handler: variable tick interval for game timing

        This handler will advance the game if it is not paused and update the
        status bar with the results (live cell count may change).

        This handler will also change the timer period if it has changed.

        Args:
            event: [wx.TimerEvent]
        """
        if not self.is_paused:
            self.live_cells = self.pnlGrid.advance_generation()
            self.update_status_bar()
        if self.is_reset_timer:
            self.is_reset_timer = False
            self.tmrGame.Start(self.timer_period_ms)
        event.Skip()


    def on_size(self, event:wx.SizeEvent):
        """EVT_SIZE event handler

        This handles resizing of the frame. Since this event may be called
        before the CGOL frame object is actually constructed, it checks the
        object and returns imediately if it is not constructed.

        Args:
            event: [wx.SizeEvent]

        Notes:
            Call method .SendSizeEvent() to trigger this function via code,
            for instance after loading a new game grid.
        """

        event.Skip()

        if not hasattr(self, "is_initialized") or not self.is_initialized:
            # --- catch the wxPython EVT_SIZE lifecycle bug ---
            return

        container_sizer = self.pnlGrid.GetContainingSizer()
        if not container_sizer:
            return

        sizer_size = container_sizer.GetSize()
        w_avail = sizer_size.width
        h_avail = sizer_size.height

        if w_avail <= 0 or h_avail <= 0:
            return

        w_cell_max = w_avail // self.cols
        h_cell_max = h_avail // self.rows

        cell_size = min(w_cell_max, h_cell_max)
        if cell_size < 1: cell_size = 1

        self.pnlGrid.configure(cell_wh=(cell_size, cell_size))
        w_panel = self.cols * cell_size
        h_panel = self.rows * cell_size

        self.pnlGrid.SetMinSize(wx.Size(w_panel, h_panel))
        self.pnlGrid.Refresh()


    def on_click_play(self, event:wx.CommandEvent):
        """EVT_TOOL handler for the play/pause button

        Args:
            event: [wx.CommandEvent]
        """
        self.is_paused = not self.is_paused
        self.pnlGrid.is_paused = self.is_paused
        if self.is_paused:
            self.show_message("Game paused...")
        else:
            self.show_message("Game started...")
        self.update_toolbar()
        self.update_status_bar()
        event.Skip()


    def on_click_step(self, event:wx.CommandEvent):
        """EVT_TOOL handler for the single step button

        Args:
            event: [wx.CommandEvent]
        """
        if self.is_paused:
            self.live_cells = self.pnlGrid.advance_generation()
            self.update_status_bar()
            self.show_message("Advanced one step...")
        self.update_status_bar()
        event.Skip()


    def on_click_slow(self, event:wx.CommandEvent):
        """EVT_TOOL handler for the game slower button

        Args:
            event: [wx.CommandEvent]
        """
        pos = self.sldSpeed.GetValue()
        CHG = CGOL.SLIDER_CHG
        pos = int(math.floor(pos/CHG)*CHG) - CHG
        if pos < 0:  pos = 0
        self.sldSpeed.SetValue(pos)
        tmr_ms = CGOL.get_timer_ms(pos)
        self.timer_period_ms = tmr_ms
        self.is_reset_timer = True
        if pos == 0:
            self.show_message("At slowest speed...")
        else:
            self.show_message("Slowed it down a notch...")
        event.Skip()


    def on_click_fast(self, event:wx.CommandEvent):
        """EVT_TOOL handler for the game faster button

        Args:
            event: [wx.CommandEvent]
        """
        pos = self.sldSpeed.GetValue()
        CHG = CGOL.SLIDER_CHG
        pos = int(math.ceil(pos/CHG)*CHG) + CHG
        if pos > CGOL.SLIDER_MAX: pos = CGOL.SLIDER_MAX
        self.sldSpeed.SetValue(pos)
        tmr_ms = CGOL.get_timer_ms(pos)
        self.timer_period_ms = tmr_ms
        self.is_reset_timer = True
        if pos == CGOL.SLIDER_MAX:
            self.show_message("At fastest speed...")
        else:
            self.show_message("Sped it up a notch...")
        event.Skip()


    def on_speed_scroll(self, event:wx.ScrollEvent):
        """EVT_SLIDER handler for the game speed slider

        Args:
            event: [wx.ScrollEvent]
        """
        pos = self.sldSpeed.GetValue()
        tmr_ms = CGOL.get_timer_ms(pos)
        self.timer_period_ms = tmr_ms
        self.is_reset_timer = True
        event.Skip()


    def on_status_click(self, event:wx.MouseEvent):
        """EVT_LEFT_DOWN or EVT_RIGHT_DOWN handler for the status bar

        Clicking the grid size field will open a dialog to resize the grid.

        Args:
            event: [wx.MouseEvent]
        """
        # get the click position and determine which field was clicked
        pos_x = event.GetPosition().x
        idx_field = -1  # clicked field idx

        for idx in range(CGOL.STATUS.N_FIELDS):
            rect = self.stabStatusBar.GetFieldRect(idx)
            if rect.x <= pos_x < (rect.x + rect.width):
                idx_field = idx
                break

        # act depending upon the field
        if idx_field == CGOL.STATUS.IDX.FIELD_GRID:
            # edit grid size
            self.show_message("Resizing grid...")
            dialog = dlgGetDims(self)
            dialog.spinRows.SetValue(self.rows)
            dialog.spinCols.SetValue(self.cols)
            dialog.SetTitle("Resize: enter dimensions")
            if (result := dialog.ShowModal()) == wx.ID_OK:
                rows_gen = dialog.spinRows.GetValue()
                cols_gen = dialog.spinCols.GetValue()
                self.pnlGrid.resize_game(size=(rows_gen, cols_gen))
                self.rows, self.cols = self.pnlGrid.size()
                self.live_cells = self.pnlGrid.live_cells
                self.SendSizeEvent()
                self.update_status_bar()
                self.Refresh()

        event.Skip()


    def on_game_select(self, event:wx.CommandEvent):
        """EVT_COMBOBOX for the game select combo box

        Args:
            event: [wx.CommandEvent]
        """
        n_action_items = len(CGOL.COMBO_ACTION_ITEMS)
        sel = self.cmbGame.GetSelection()
        if sel >= n_action_items:
            self.is_paused = True
            self.update_toolbar()
            idx = sel - n_action_items
            self.pnlGrid.load_preset(idx)
        else:
            if sel == 0:
                # New game
                self.show_message("Creating new game...")
                dialog = dlgGetDims(self)
                dialog.SetTitle("New game: enter dimensions")
                if (result := dialog.ShowModal()) == wx.ID_OK:
                    rows_gen = dialog.spinRows.GetValue()
                    cols_gen = dialog.spinCols.GetValue()
                    self.pnlGrid.new_game(size=(rows_gen, cols_gen))
                    self.rows, self.cols = self.pnlGrid.size()
                    #self.SendSizeEvent()
                    #self.Refresh()
            elif sel == 1:
                # Load game
                self.show_message("Loading game...")
                self.pnlGrid.load_file()
            elif sel == 21:
                # Save game
                self.show_message("Saving game...")
                self.pnlGrid.save_file()
            games_list = self.pnlGrid.games_list
            self.cmbGame.Set(CGOL.COMBO_ACTION_ITEMS + games_list)
            name_of_game = self.pnlGrid.name_of_game
            if name_of_game in games_list:
                idx = games_list.index(name_of_game) + n_action_items
                self.cmbGame.SetSelection(idx)

        self.rows, self.cols = self.pnlGrid.size()
        self.update_status_bar()
        self.live_cells = self.pnlGrid.live_cells
        self.show_message(f"Game: {self.pnlGrid.name_of_game}")
        self.SendSizeEvent()
        self.Refresh()
        event.Skip()


    def on_warp_check(self, event:wx.CommandEvent):
        """EVT_CHECKBOX for the "warp" checkbox

        Args:
            event: [wx.CommandEvent]
        """
        self.is_warp = self.chkWarpEdge.GetValue()
        # TODO: implement
        if self.is_warp:
            self.show_message("Let's do the time warp again...")
        else:
            self.show_message("Let them disintegrate...")
        event.Skip()


    def on_take_snap(self, event:wx.CommandEvent):
        """EVT_TOOL handler for the take snapshot button

        Args:
            event: [wx.CommandEvent]
        """
        # TODO: take snapshot will capture text to clipboard, restore will restore from clipboard
        self.show_message("Took snapshot of grid...")
        self.pnlGrid.take_snapshot()
        event.Skip()


    def on_restore_snap(self, event:wx.CommandEvent):
        """EVT_TOOL handler for the restore snapshot button

        Args:
            event: [wx.CommandEvent]
        """
        self.show_message("Restored snapshot to grid...")
        self.pnlGrid.restore_snapshot()
        event.Skip()


    def on_click_about(self, event:wx.CommandEvent):
        """EVT_TOOL handler for the about button

        Args:
            event: [wx.CommandEvent]
        """
        self.show_message("About this program...")
        self.show_about_dialog()
        # omit event.Skip() here


    def show_about_dialog(self):
        """Create and show an About dialog box
        """
        # Create a modern Info layout
        info = wx.adv.AboutDialogInfo()
        info.SetName("Conway's Game of Life")
        info.SetVersion(f"{CGOL.VERSION}")
        info.SetCopyright("Copyright © 2026 Kerry S Martin")
        info.AddDeveloper("Kerry S Martin")
        info.SetWebSite("mailto:wssm243@gmail.com?subject=CGOL", "Contact the Author via Email")
        info.SetLicense(
    "This software is released into the public domain under The Unlicense.\n\n"
    "Anyone is free to copy, modify, publish, use, compile, sell, or "
    "distribute this software, either in source code form or as a compiled "
    "binary, for any purpose, commercial or non-commercial, and by any means."
        )

        # Format your shortcut guide using newline breaks
        shortcuts = (
            "\nKeyboard Shortcuts:\n"
            "• Spacebar - Play / pause\n"
            "• a - Advance one step\n"
            "• t - Take snapshot\n"
            "• r - Restore snapshot\n"
            "• < - Shorter interval\n"
            "• > - Longer interval"
        )
        info.SetDescription(shortcuts)

        # Trigger the native OS dialog
        wx.adv.AboutBox(info)


# ------------------------------------------------------------------------------
# Main program entry point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = wx.App()
    #if not wx.Image.FindHandler(wx.BITMAP_TYPE_PNG):
    #    wx.InitAllImageHandlers()
    frame = CGOL(None)
    frame.Show()
    app.MainLoop()


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************