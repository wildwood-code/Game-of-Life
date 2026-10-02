/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : grid_menu.cpp
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file contains the implementation of the CGOL grid context menu.
*
*  Change log:
*    2026-09-27  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#include "grid_menu.h"


/// @brief Constructor for grid context menu class.
/// @param parent wxGrid object that is the parent of this context menu
GridContextMenu::GridContextMenu(wxPanel* parent)
: m_parent(parent), m_menu(wxMenu())
{
    m_map.clear();
    m_result = StructureSpec::NONE;

    for (StructureSpec entry : AppConfig::CGOL_CONTEXT_LIST)
    {
        if (entry.name.empty())
        {
            m_menu.AppendSeparator();
        }
        else
        {
            wxMenuItem* item = m_menu.Append(wxID_ANY, entry.name);
            m_map.insert_or_assign(item->GetId(), entry);
        }
    }
    m_menu.Bind(wxEVT_MENU, &GridContextMenu::on_menu_click, this);
}


/// @brief Call this to show the popup menu at the given position
/// @param pos position at which context menu will be opened.
/// @return Reference to the result from the selection; STRUCTURE_SPEC EMPTY if
/// there was no selection made.
StructureSpec& GridContextMenu::show_context_menu(wxPoint& pos)
{
    m_result = StructureSpec::NONE;
    m_parent->PopupMenu(&m_menu, pos);
    return m_result;
}


/// @brief wxEVT_MENU handler for the context menu
/// @param event
void GridContextMenu::on_menu_click(wxCommandEvent& event)
{
    int item_id = event.GetId();
    if (m_map.contains(item_id))
    {
        m_result = m_map.at(item_id);
    }
}


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/