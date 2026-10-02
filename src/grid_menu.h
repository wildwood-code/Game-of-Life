/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : grid_menu.h
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file contains the interface for the CGOL grid context menu.
*
*  Change log:
*    2026-09-27  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#pragma once

#include "app_config.h"
#include <wx/menu.h>
#include <wx/panel.h>
#include <unordered_map>

class GridContextMenu
{
protected:
    wxPanel* m_parent;
    wxMenu   m_menu;
    StructureSpec m_result;
    std::unordered_map<int,StructureSpec> m_map;

public:
    GridContextMenu(wxPanel* parent);
    StructureSpec& show_context_menu(wxPoint& pos);

protected:
    void on_menu_click(wxCommandEvent& event);
};


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/