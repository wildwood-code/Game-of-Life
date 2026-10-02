/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : about.cpp
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file implements the about dialog.
*
*  Change log:
*    2026-09-25  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#include "about.h"
#include "app_config.h"
#include "cgol_version.h"
#include <wx/aboutdlg.h>


/// @brief Show the about dialog for this application
void show_about_dialog()
{
    wxAboutDialogInfo info;
    info.SetName("Conway's Game of Life");
    info.SetVersion(VERSION_STRING);
    info.SetCopyright(CGOL_STRING::FromUTF8("Copyright \u00A9 2026 Kerry S Martin"));
    info.AddDeveloper("Kerry S Martin");
    info.SetWebSite("mailto:wssm243@gmail.com?subject=CGOL", "Contact the Author via Email");
    info.SetLicense(
    "This software is released into the public domain under The Unlicense.\n\n"
    "Anyone is free to copy, modify, publish, use, compile, sell, or "
    "distribute this software, either in source code form or as a compiled "
    "binary, for any purpose, commercial or non-commercial, and by any means."
    );
    info.SetDescription(
    "This C++ program implements a simple zero-player game\n"
    "known as Conway's Game of Life (CGoL). CGoL was devised\n"
    "by John Horton Conway in 1970.\n"
    "https://en.wikipedia.org/wiki/Conway's_Game_of_Life\n"
    "\nKeyboard Shortcuts:\n"
    "spacebar - Play / pause\n"
    "a - Advance one step\n"
    "s - Advance one step\n"
    "t - Take snapshot\n"
    "r - Restore snapshot\n"
    "g - Toggle grid on/off\n"
    "w - Toggle edge warp\n"
    "< - Shorter interval\n"
    "> - Longer interval"
    );

    wxAboutBox(info);
}


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/