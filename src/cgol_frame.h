/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : cgol_frame.h
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file defines the interface for the main form/window of the GUI.
*
*  Change log:
*    2026-09-21  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#pragma once

#include "generated/generated_ui.h"
#include <wx/bitmap.h>
#include <wx/timer.h>


class wxFrame_CGOL : public wxFrame_Main
{
public:
    // interface: construction and destruction
    wxFrame_CGOL(CGOL_STRING filename);
    virtual ~wxFrame_CGOL() = default;

protected:
    // member variables
    bool is_initialized;
    bool is_reset_timer;
    int timer_period_ms;

    RulesList m_rules_list;

    // bitmap images
    wxBitmap bitmap_play;
    wxBitmap bitmap_pause;

    // timers and messages
    wxTimer* p_taskTimer;
    wxTimer* p_gameTimer;
    int ctr_message;

    // tool and keypress ids
    int id_tool_play;
    int id_tool_step;
    int id_tool_warp;
    int id_tool_warp_key;
    int id_tool_grid;
    int id_tool_grid_key;
    int id_tool_faster;
    int id_tool_slower;
    int id_tool_snap;
    int id_tool_restore;
    int id_tool_about;

    // functions passed to the contained panel
    std::function<void()> m_fnUpdateStatus;
    std::function<void(const char*, int)> m_fnShowMessage;

    // event handlers
    void on_size(wxSizeEvent& event);
    void on_click_play(wxCommandEvent& event);
    void on_click_step(wxCommandEvent& event);
    void on_click_warp(wxCommandEvent& event);
    void on_click_grid(wxCommandEvent& event);
    void on_click_faster(wxCommandEvent& event);
    void on_click_slower(wxCommandEvent& event);
    void on_click_snap(wxCommandEvent& event);
    void on_click_restore(wxCommandEvent& event);
    void on_click_about(wxCommandEvent& event);
    void on_select_game(wxCommandEvent& event);
    void on_select_rule(wxCommandEvent& event);
    void on_scroll_speed(wxCommandEvent& event);
    void on_click_status(wxMouseEvent& event);
    void on_task_timer(wxTimerEvent& event);
    void on_game_timer(wxTimerEvent& event);

    // event sub-handlers
    void on_click_status_rules();
    void on_click_status_grid();
    void on_click_status_live();
    void on_click_status_state();
    void on_select_preset(int preset);
    void on_new_game();
    void on_load_game();
    void on_save_game();

    // support functions
    void set_tool_image(int id, wxBitmap& bitmap);
    void update_toolbar();
    void update_status_bar();
    void show_message(CGOL_STRING const& message, int time_ms=0);
    void register_rules(Rules rules=CGOL_EMPTY_STRING);
    void refresh_tool_and_status(CGOL_STRING const& msg=wxEmptyString);
    void refresh_games_list();
    void refresh_rules_list();


    // static support functions
    static int get_timer_ms(int slider);
    static int get_slider_pos(int timer_ms);
    static void copy_text_to_clipboard(CGOL_STRING const& clip);
    static CGOL_STRING get_text_from_clipboard();
};


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/