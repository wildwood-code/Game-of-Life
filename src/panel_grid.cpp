/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : panel_grid.cpp
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file implements the wxPanel used to display the game grid.
*
*  Change log:
*    2026-09-21  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#include "panel_grid.h"
#include <wx/dcmemory.h>
#include <wx/dcbuffer.h>
#include <wx/filedlg.h>
#include <wx/filename.h>


/// @brief Constructor for the game grid panel
/// @param parent  parent window
/// @param winid   default=wxID_ANY
/// @param pos     default=wxDefaultPosition
/// @param size    default=wxDefaultSize
/// @param style   default=wxTAB_TRAVERSAL|wxNO_BORDER
wxPanel_Grid::wxPanel_Grid(wxWindow* parent,
    wxWindowID winid,
    const wxPoint& pos,
    const wxSize& size,
    long style)
    : wxPanel(parent, winid, pos, size, style),
      m_game(CGOL_Game()),
      is_paused(true),
      is_grid_visible(false),
      cell_w(AppConfig::CELL_W),
      cell_h(AppConfig::CELL_H),
      color_background(AppConfig::BACKGROUND_COLOR),
      color_grid(AppConfig::GRID_COLOR),
      color_live_cell(AppConfig::LIVE_CELL_COLOR),
      color_highlight(AppConfig::HIGHLIGHT_COLOR),
      fn_show_message(nullptr),
      fn_update_status(nullptr),
      highlight_cell(array_index_t::INVALID),
      m_menu(GridContextMenu(this)),
      buffer_bitmap(wxBitmap(1,1))
{
    auto shape = m_game.get_shape();

    SetMinSize(wxSize(cell_w*shape.cols, cell_h*shape.rows));
    Bind(wxEVT_PAINT, &wxPanel_Grid::on_paint, this);
    Bind(wxEVT_SIZE, &wxPanel_Grid::on_size, this);
    Bind(wxEVT_ERASE_BACKGROUND, &wxPanel_Grid::on_erase_background, this);
    Bind(wxEVT_LEFT_DOWN, &wxPanel_Grid::on_left_click, this);
    Bind(wxEVT_RIGHT_DOWN, &wxPanel_Grid::on_right_click, this);
    SetDoubleBuffered(true);
    sync_from_engine();
}


/// @brief Load a preset game
/// @param preset 0-based preset index
/// @return game designator
const Designator& wxPanel_Grid::load_preset(int preset)
{
    Designator result = m_game.load_preset(preset);
    if (result)
        sync_from_engine();
    return m_game.get_designator();
}


/// @brief Create a new, blank game
/// @param shape {rows, cols} shape of the new game
/// @return game designator
const Designator& wxPanel_Grid::new_game(array_shape_t shape)
{
    m_game.new_game(shape);
    sync_from_engine();
    return m_game.get_designator();
}


/// @brief Load a file either from the provided filename or via a dialog
/// @param filename default="" -> choose file via a dialog
/// @return game designator
const Designator& wxPanel_Grid::load_file(CGOL_STRING const& filename)
{
    Designator result = {0, 0, wxEmptyString};

    if (!filename.empty())
    {
        result = m_game.load_file(filename);
    }
    else
    {
        wxFileDialog dlg(this,
            "Open file...",
            wxFileName::GetCwd(),
            wxEmptyString,
            "CGOL files (*.cgol)|*.cgol|All files (*.*)|*.*",
            wxFD_OPEN|wxFD_FILE_MUST_EXIST);

        if (dlg.ShowModal()==wxID_OK)
        {
            result = m_game.load_file(dlg.GetPath());
        }
    }

    if (result)
        sync_from_engine();

    return m_game.get_designator();
}


bool wxPanel_Grid::save_file()
{
    bool result = false;

    wxFileDialog dlg(this,
        "Save file...",
        wxFileName::GetCwd(),
        wxEmptyString,
        "CGOL files (*.cgol)|*.cgol|All files (*.*)|*.*",
        wxFD_SAVE|wxFD_OVERWRITE_PROMPT);

    if (dlg.ShowModal()==wxID_OK)
    {
        CGOL_STRING filename = dlg.GetPath();
        result = m_game.save_file(filename);
    }

    return result;
}


/// @brief wxEVT_LEFT_DOWN handler: click to toggle grid cells
/// @param event wxMouseEvent
void wxPanel_Grid::on_left_click(wxMouseEvent& event)
{
    if (is_paused)
    {
        // get the exact pixel coordinate where the user clicked
        wxPoint pos = event.GetPosition();
        int click_x = pos.x;
        int click_y = pos.y;

        // divide by the cell size to get the grid row/column
        int col = click_x / cell_w;
        int row = click_y / cell_h;

        // toggle the cell state
        array_shape_t shape = m_game.get_shape();

        if (shape.inside(row, col))
        {
            bool cell = !m_game(row, col);
            m_game(row, col) = cell;
            grid_data(row, col) = cell;
            m_game.refresh_live_cell_count();
            render_grid_to_buffer();
            update_status();
            Refresh();
        }
    }
    else
    {
        show_message("Pause to edit grid...");
    }

    event.Skip();
}


/// @brief wxEVT_RIGHT_DOWN handler for the grid panel
/// @param event
void wxPanel_Grid::on_right_click(wxMouseEvent& event)
{
    if (is_paused)
    {
        wxPoint pos = event.GetPosition();
        int click_col = pos.x / cell_w;
        int click_row = pos.y / cell_h;
        array_shape_t shape = m_game.get_shape();

        if (shape.outside(click_row, click_col))
            return;

        highlight_cell = {click_row, click_col};
        render_grid_to_buffer();
        Refresh();

        StructureSpec result = m_menu.show_context_menu(pos);

        if (result)
        {
            if (result.head.r==-1 && result.head.c==0)
            {
                m_game.clear();
                show_message("Cleared the grid...");
            }
            else
            {
                array_index_t pos_at = {click_row-result.head.r, click_col-result.head.c};
                m_game.add_pattern_at(result.pattern, pos_at);
                CGOL_STRING msg = CGOL_FORMAT("Added %s...", result.name.Lower());
                show_message(msg);
            }
        }

        highlight_cell = array_index_t::INVALID;
        sync_from_engine();
        render_grid_to_buffer();
        update_status();
        Refresh();
    }
    else
    {
        show_message("Pause to access menu...");
    }
}


/// @brief wxEVT_SIZE handler for the grid panel
/// @param event
void wxPanel_Grid::on_size(wxSizeEvent& event)
{
    wxSize size = GetClientSize();
    if (size.x>0 && size.y>0)
    {
        buffer_bitmap = wxBitmap(size);
        render_grid_to_buffer();
    }
    event.Skip();
}


/// @brief wxEVT_PAINT handler for the grid panel
/// @param event
void wxPanel_Grid::on_paint(wxPaintEvent& event)
{
    wxBufferedPaintDC(this, buffer_bitmap);
    event.Skip();
}


/// @brief wxEVT_ERASE_BACKGROUND handler for the grid panel
/// @param event
void wxPanel_Grid::on_erase_background(wxEvent& event)
{
    event.Skip();
}


/// @brief Advance the game one generation
/// @return live cell count
size_t wxPanel_Grid::advance_generation()
{
    size_t live_cells = m_game.advance_generation();
    sync_from_engine();
    render_grid_to_buffer();
    return live_cells;
}


/// @brief Synchronize the panel data grid from the game engine data grid
void wxPanel_Grid::sync_from_engine()
{
    grid_data = m_game.get_grid_data();
    Refresh();
}


/// @brief Display a momentary message in the parent status bar
/// @param message text of message to display
void wxPanel_Grid::show_message(CGOL_STRING const& message)
{
    if (fn_show_message)
        fn_show_message(message, 0);
}


/// @brief Update the parent status bar
void wxPanel_Grid::update_status()
{
    if (fn_update_status)
        fn_update_status();
}


/// @brief Render the grid to the DC buffer
void wxPanel_Grid::redraw_grid()
{
    render_grid_to_buffer();
}


/// @brief Set the rules for the game
/// @param rules rules in B/S form (e.g. "B3/S23")
void wxPanel_Grid::set_rules(Rules rules)
{
    m_game.set_rules(rules);
}


/// @brief Take a snapshot of the grid and return as a CGOL game string
/// @return CGOL game string
CGOL_STRING wxPanel_Grid::take_snapshot(CGOL_STRING name) const
{
    return m_game.get_snapshot(name);
}


/// @brief Restore a snapshot to the grid
/// @param snap snapshot of the grid (text)
/// @return true if restored; false otherwise
bool wxPanel_Grid::restore_shapshot(CGOL_STRING const& snap)
{
    bool result = false;
    if (m_game.set_snapshot(snap))
    {
        sync_from_engine();
        Refresh();
        result = true;
    }

    return result;
}


/// @brief Resize the game to the given shape
/// @param shape {rows, cols}
void wxPanel_Grid::resize_game(array_shape_t const& shape)
{
    m_game.resize(shape);
    sync_from_engine();
    array_shape_t new_shape = m_game.get_shape();
    SetMinSize(wxSize(cell_w*new_shape.cols, cell_h*new_shape.rows));
}


/// @brief Render the grid to the DC buffer
void wxPanel_Grid::render_grid_to_buffer()
{
    auto [rows, cols] = grid_data.shape();
    int r, c;
    int x, y;

    // start with a blank canvas
    wxMemoryDC dc(buffer_bitmap);
    dc.SetBackground(wxBrush(wxColour(color_background)));
    dc.Clear();

    // configure the "live cell" brush and pen
    dc.SetBrush(wxBrush(wxColour(color_live_cell)));
    dc.SetPen(*wxTRANSPARENT_PEN);

    // draw every live cell
    for (r=0; r<rows; ++r)
    {   for (c=0; c<cols; ++c)
        {
            if (grid_data(r,c))
            {
                x = c * cell_w;
                y = r * cell_h;
                dc.DrawRectangle(x, y, cell_w, cell_h);
            }
        }
    }

    // draw highlight, if any
    if (highlight_cell)
    {
        dc.SetBrush(wxBrush(wxColour(color_highlight)));
        auto [hr, hc] = highlight_cell;
        x = hc * cell_w;
        y = hr * cell_h;
        dc.DrawRectangle(x, y, cell_w, cell_h);
    }

    // draw the grid, if visible
    if (is_grid_visible)
    {
        wxPenInfo info(wxColour(color_grid), 1, wxPENSTYLE_SOLID);
        dc.SetPen(wxPen(info));
        int x0 = 0;
        int x2 = cols*cell_w;
        int y0 = 0;
        int y2 = rows*cell_h;
        wxPoint p0, p2;
        p0.x = x0;
        p2.x = x2;
        for (r=0; r<=rows; ++r)
        {
            y = r * cell_h;
            p0.y = y;
            p2.y = y;
            dc.DrawLine(p0, p2);
        }
        p0.y = y0;
        p2.y = y2;
        for (c=0; c<=cols; ++c)
        {
            x = c * cell_w;
            p0.x = x;
            p2.x = x;
            dc.DrawLine(p0, p2);
        }
    }
}


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/