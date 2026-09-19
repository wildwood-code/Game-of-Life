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
#  Change log:
#    2026-09-05  KSM  Created
#    2026-09-09  KSM  Updated version to 1.1 and later to 1.2
#    2026-09-11  KSM  Implemented rules select/change; v1.3
#    2026-09-13  KSM  Consolidated redundant rows, cols, name variables; v1.4
#                     Added new games
#    2026-09-17  KSM  Added grid context menu; v1.5
#    2026-09-18  KSM  Added grid and grid on/off; fixed live cell count; v1.6
#    2026-09-18  KSM  Fixed live cell count after adding structure
#                     Moved all binds out of generated code to this file
#    2026-09-18  KSM  Added ability to load .cgol file passed as argument
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
# ******************************************************************************
# TODO: Feature request
#  Puffer train (\bigger grid?)  https://en.wikipedia.org/wiki/Puffer_train
#  Minor grid drawing issue: some blank space or cut grid on the bottom row
# ******************************************************************************

import wx
import sys
from cgol_frame import CGOL_frame


# ------------------------------------------------------------------------------
# Main program entry point
# ------------------------------------------------------------------------------

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    app = wx.App()
    frame = CGOL_frame(None, filename)
    frame.Show()
    app.MainLoop()


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************