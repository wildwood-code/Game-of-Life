/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : panel_grid.h
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file defines the interface for the wxPanel used to display the
*    game grid.
*
*  Change log:
*    2026-09-21  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#pragma once

#include "app_config.h"
#include <wx/panel.h>
#include <wx/bitmap.h>
#include "cgol_game.h"
#include "grid_menu.h"


class wxPanel_Grid : public wxPanel
{
public:
    // game settings
    bool is_paused;
    bool is_grid_visible;

protected:
    // game and grid data
    CGOL_Game m_game;
    int cell_w;
    int cell_h;
    uint32_t color_live_cell;
    uint32_t color_grid;
    uint32_t color_background;
    uint32_t color_highlight;
    CellArray grid_data;
    array_index_t highlight_cell;
    wxBitmap buffer_bitmap;
    GridContextMenu m_menu;

    // callback functions from parent
    std::function<void()> fn_update_status;
    std::function<void(CGOL_STRING const&, int)> fn_show_message;

public:
    // construction, destruction, and configuration
    wxPanel_Grid(wxWindow* parent,
        wxWindowID winid = wxID_ANY,
        const wxPoint& pos = wxDefaultPosition,
        const wxSize& size = wxDefaultSize,
        long style = wxTAB_TRAVERSAL|wxNO_BORDER);

    virtual ~wxPanel_Grid() = default;

    void register_functions(std::function<void()> pfn_status, std::function<void(CGOL_STRING const&, int)> pfn_message)
    {
        fn_update_status = std::move(pfn_status);
        fn_show_message = std::move(pfn_message);
    }

    void set_wh(int w, int h) { cell_w = w; cell_h = h; }

    // game creation, snapshots, and saving
    const Designator& load_preset(int preset);
    const Designator& new_game(array_shape_t shape);
    const Designator& load_file(CGOL_STRING const& filename=wxEmptyString);
    bool save_file();
    CGOL_STRING take_snapshot(CGOL_STRING name="") const;
    bool restore_shapshot(CGOL_STRING const& snap);

    // game information
    CGOL_STRING name_of_game() const { return m_game.get_name(); }
    void set_name_of_game(CGOL_STRING const& name) { m_game.set_name(name); }
    Rules get_rules() const { return m_game.get_rules(); }
    void get_rule_spec(RuleSpec& spec) const { m_game.get_rule_spec(spec); }
    void set_rule_spec(const RuleSpec& spec) { m_game.set_rule_spec(spec); }
    void set_rules(Rules rules);
    GamesNamesList get_games_names_list() const noexcept { return m_game.get_games_names_list(); }
    RulesList get_rules_list() const noexcept { return m_game.get_rules_list(); }
    bool is_game_loaded() const { CGOL_STRING name = m_game.get_name(); return !name.empty(); }
    array_shape_t shape() const { return m_game.get_shape(); }
    size_t get_live_cell_count() { return m_game.get_live_cell_count(); }

    // game settings
    void set_warp(bool warp) { m_game.set_warp(warp); }
    bool get_warp() const { return m_game.is_warp(); }
    bool toggle_warp() { bool warp = !m_game.is_warp(); m_game.set_warp(warp); return warp; }

    // game modification
    void resize_game(array_shape_t const& shape);
    void redraw_grid();

    // playing the game
    size_t advance_generation();

protected:
    // event handlers
    void on_paint(wxPaintEvent& event);
    void on_size(wxSizeEvent& event);
    void on_erase_background(wxEvent& event);
    void on_left_click(wxMouseEvent& event);
    void on_right_click(wxMouseEvent& event);

    // support functions
    void show_message(CGOL_STRING const& message);
    void update_status();
    void sync_from_engine();
    void render_grid_to_buffer();
};


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/