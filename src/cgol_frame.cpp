/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : cgol_frame.cpp
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file implements the main window (form) for the GUI.
*
*  Change log:
*    2026-09-21  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#include "app_config.h"
#include "cgol_frame.h"
#include "panel_grid.h"
#include "cgol_images.h"
#include "about.h"
#include "generated/generated_ui.h"
#include "rules_dialog.h"
#include "size_dialog.h"
#include <cmath>
#include <algorithm>
#include <iterator>
#include <wx/textdlg.h>
#include <functional>
#include <wx/clipbrd.h>
#include <wx/dataobj.h>


enum STATUS_FIELD
{
    STATE = 0,
    LIVE_COUNT = 1,
    GRID_SIZE = 2,
    RULES_SET = 3,
    MESSAGE = 4,
    N_FIELD_COUNT = 5
};

int const STATUS_FIELD_WIDTHS[] = { 80, 120, 80, 80, -1 };


const GamesNamesList ACTION_ITEMS =
{   // !!! UPDATE IDX_ACTION_ITEMS BELOW !!!
    "(New game)",
    "(Load game)",
    "(Save game)"
};  // !!! UPDATE IDX_ACTION_ITEMS BELOW !!!

const CGOL_STRING UNSAVED_GAME = "(Unsaved game)";

enum IDX_ACTION_ITEMS
{
    NEW_GAME = 0,
    LOAD_GAME = 1,
    SAVE_GAME = 2,
    N_ACTION_ITEMS = 3
};


/// @brief CGOL main frame constructor
/// @param filename optional filename. default=""
/// @note If a filename is passed, CGOL main frame will open that game;
/// otherwise, it will open the configured initial preset.
wxFrame_CGOL::wxFrame_CGOL(CGOL_STRING filename)
    : wxFrame_Main(nullptr)
{
    // --- catch the wxPython lifecycle trap in on_size() ---
    is_initialized = false;

    // -- begin form initialization ---
    tbarMain->Realize();
    Layout();

    // --- game settings ---
    pnlGrid->is_paused = true;
    pnlGrid->set_warp(true);
    pnlGrid->is_grid_visible = false;

    // --- pass bound functions to panel ---
    m_fnUpdateStatus =  [this]() { update_status_bar(); };
    m_fnShowMessage =
        [this](const char* msg, int val) { show_message(msg, val); };
    pnlGrid->register_functions(m_fnUpdateStatus, m_fnShowMessage);

    // --- set the application icons ---
    wxIconBundle app_icons = wxIconBundle();
    app_icons.AddIcon(get_icon(CGOL_game_icon_16x16, LEN_CGOL_game_icon_16x16));
    app_icons.AddIcon(get_icon(CGOL_game_icon_24x24, LEN_CGOL_game_icon_24x24));
    app_icons.AddIcon(get_icon(CGOL_game_icon_32x32, LEN_CGOL_game_icon_32x32));
    app_icons.AddIcon(get_icon(CGOL_game_icon_48x48, LEN_CGOL_game_icon_48x48));
    app_icons.AddIcon(get_icon(CGOL_game_icon_128x128, LEN_CGOL_game_icon_128x128));
    app_icons.AddIcon(get_icon(CGOL_game_icon_256x256, LEN_CGOL_game_icon_256x256));
    SetIcons(app_icons);

    // --- load all tool images ---
    bitmap_play = get_bitmap(image_play, LEN_IMAGE_PLAY);
    bitmap_pause = get_bitmap(image_pause, LEN_IMAGE_PAUSE);
    wxBitmap bitmap_step = get_bitmap(image_step, LEN_IMAGE_STEP);
    wxBitmap bitmap_warp = get_bitmap(image_warp, LEN_IMAGE_WARP);
    wxBitmap bitmap_grid = get_bitmap(image_grid, LEN_IMAGE_GRID);
    wxBitmap bitmap_faster = get_bitmap(image_faster, LEN_IMAGE_FASTER);
    wxBitmap bitmap_slower = get_bitmap(image_slower, LEN_IMAGE_SLOWER);
    wxBitmap bitmap_snap = get_bitmap(image_snap, LEN_IMAGE_SNAP);
    wxBitmap bitmap_restore = get_bitmap(image_restore, LEN_IMAGE_RESTORE);
    wxBitmap bitmap_about = get_bitmap(image_about, LEN_IMAGE_ABOUT);

    id_tool_play = toolPlay->GetId();
    id_tool_step = toolStep->GetId();
    id_tool_warp = toolWarp->GetId();
    id_tool_warp_key = wxNewId();
    id_tool_grid = toolGrid->GetId();
    id_tool_grid_key = wxNewId();
    id_tool_faster = toolFaster->GetId();
    id_tool_slower = toolSlower->GetId();
    id_tool_snap = toolTakeSnap->GetId();
    id_tool_restore = toolRestoreSnap->GetId();
    id_tool_about = toolAbout->GetId();

    set_tool_image(id_tool_step, bitmap_step);
    set_tool_image(id_tool_warp, bitmap_warp);
    set_tool_image(id_tool_grid, bitmap_grid);
    set_tool_image(id_tool_faster, bitmap_faster);
    set_tool_image(id_tool_slower, bitmap_slower);
    set_tool_image(id_tool_snap, bitmap_snap);
    set_tool_image(id_tool_restore, bitmap_restore);
    set_tool_image(id_tool_about, bitmap_about);
    update_toolbar();  // sets the play/pause tool image

    if (!filename.empty())
    {   // --- Try to load a game from a file ---
        pnlGrid->load_file(filename);
    }

    if (!pnlGrid->is_game_loaded())
    {   // --- No game has been loaded yet, so load the preset game ---
        pnlGrid->load_preset(AppConfig::INITIAL_GAME_INDEX);
    }

    // --- Update the combo box with the games list and select current game ---
    refresh_games_list();

    // --- configure rule selector combo box ---
    refresh_rules_list();

    // --- configure status bar ---
    stabStatusBar->SetFieldsCount(STATUS_FIELD::N_FIELD_COUNT);
    stabStatusBar->SetStatusWidths(STATUS_FIELD::N_FIELD_COUNT, STATUS_FIELD_WIDTHS);
    SetStatusBarPane(-1);
    update_status_bar();

    // --- bind events for this frame ---
    Bind(wxEVT_SIZE, &wxFrame_CGOL::on_size, this);

    // --- bind toolbar tools ---
    Bind(wxEVT_TOOL, &wxFrame_CGOL::on_click_play, this, id_tool_play);
    Bind(wxEVT_TOOL, &wxFrame_CGOL::on_click_step, this, id_tool_step);
    Bind(wxEVT_TOOL, &wxFrame_CGOL::on_click_warp, this, id_tool_warp);
    Bind(wxEVT_TOOL, &wxFrame_CGOL::on_click_grid, this, id_tool_grid);
    Bind(wxEVT_TOOL, &wxFrame_CGOL::on_click_faster, this, id_tool_faster);
    Bind(wxEVT_TOOL, &wxFrame_CGOL::on_click_slower, this, id_tool_slower);
    Bind(wxEVT_TOOL, &wxFrame_CGOL::on_click_snap, this, id_tool_snap);
    Bind(wxEVT_TOOL, &wxFrame_CGOL::on_click_restore, this, id_tool_restore);
    Bind(wxEVT_TOOL, &wxFrame_CGOL::on_click_about, this, id_tool_about);

    // --- bind the toggle keys ---
    Bind(wxEVT_MENU, &wxFrame_CGOL::on_click_warp, this, id_tool_warp_key);
    Bind(wxEVT_MENU, &wxFrame_CGOL::on_click_grid, this, id_tool_grid_key);

    // --- bind the controls ---
    cmbGame->Bind(wxEVT_COMBOBOX, &wxFrame_CGOL::on_select_game, this);
    cmbRules->Bind(wxEVT_COMBOBOX, &wxFrame_CGOL::on_select_rule, this);
    sldSpeed->Bind(wxEVT_SLIDER, &wxFrame_CGOL::on_scroll_speed, this);
    stabStatusBar->Bind(wxEVT_LEFT_DOWN, &wxFrame_CGOL::on_click_status, this);

    // --- setup key bindings ---
    const int num_entries = 12;
    wxAcceleratorEntry entries[num_entries];
    entries[0].Set(wxACCEL_NORMAL, WXK_SPACE, id_tool_play);
    entries[1].Set(wxACCEL_NORMAL, 'a',       id_tool_step);
    entries[2].Set(wxACCEL_NORMAL, 's',       id_tool_step);
    entries[3].Set(wxACCEL_NORMAL, 't',       id_tool_snap);
    entries[4].Set(wxACCEL_NORMAL, 'r',       id_tool_restore);
    entries[5].Set(wxACCEL_NORMAL, 'g',       id_tool_grid_key);
    entries[6].Set(wxACCEL_NORMAL, 'w',       id_tool_warp_key);
    entries[7].Set(wxACCEL_NORMAL, WXK_F1,    id_tool_about);
    entries[8].Set(wxACCEL_NORMAL, '.',       id_tool_faster);
    entries[9].Set(wxACCEL_NORMAL, ',',       id_tool_slower);
    entries[10].Set(wxACCEL_SHIFT, '.',       id_tool_faster);
    entries[11].Set(wxACCEL_SHIFT, ',',       id_tool_slower);
    wxAcceleratorTable accel(num_entries, entries);
    SetAcceleratorTable(accel);

    // --- configure message timer ---
    p_taskTimer = new wxTimer();
    ctr_message = 0;
    p_taskTimer->Bind(wxEVT_TIMER, &wxFrame_CGOL::on_task_timer, this);
    p_taskTimer->Start(AppConfig::TASK_TICK_MS, wxTIMER_CONTINUOUS);
    show_message(CGOL_EMPTY_STRING);

    // -- configure game timer and slider speed control ---
    timer_period_ms = AppConfig::TIMER_INI_MS;
    is_reset_timer = false;
    sldSpeed->SetRange(0, AppConfig::SLIDER_MAX);
    sldSpeed->SetValue(get_slider_pos(timer_period_ms));
    p_gameTimer = new wxTimer();
    p_gameTimer->Bind(wxEVT_TIMER, &wxFrame_CGOL::on_game_timer, this);
    p_gameTimer->Start(timer_period_ms, wxTIMER_CONTINUOUS);

    // --- finalize our initialization ---
    is_initialized = true;
}


/// @brief wxEVT_SIZE handler: handles frame resizing
/// @param event wxSizeEvent
void wxFrame_CGOL::on_size(wxSizeEvent& event)
{
    // since we are binding wxEVT_SIZE ourself, we should not encounter the
    // "Early Sizing / Uninitialized Object Bug".

    event.Skip();

    wxSizer* panel_sizer = szrMain;
    if (!panel_sizer)
        return;

    wxSize sizer_size = panel_sizer->GetSize();
    int w_avail = sizer_size.GetWidth();
    int h_avail = sizer_size.GetHeight();

    if (w_avail<=0 || h_avail<=0)
        return;

    array_shape_t grid_size = pnlGrid->shape();
    int rows = grid_size.rows;
    int cols = grid_size.cols;

    int w_cell_max = w_avail / cols;
    int h_cell_max = h_avail / rows;

    int cell_size = std::min(w_cell_max, h_cell_max);
    if (cell_size < 1)
        cell_size = 1;

    pnlGrid->set_wh(cell_size, cell_size);

    int w_panel = cols * cell_size;
    int h_panel = rows * cell_size;

    pnlGrid->SetMinSize(wxSize(w_panel, h_panel));
    pnlGrid->Refresh();
}


/// @brief wxEVT_TOOL handler for play/pause tool button
/// @param event wxCommandEvent
void wxFrame_CGOL::on_click_play(wxCommandEvent& event)
{
    pnlGrid->is_paused = !pnlGrid->is_paused;
    if (pnlGrid->is_paused)
        show_message("Game paused...");
    else
        show_message("Game resumed...");
    update_toolbar();
    update_status_bar();
}


/// @brief wxEVT_TOOL handler for single-step tool button
/// @param event wxCommandEvent
void wxFrame_CGOL::on_click_step(wxCommandEvent& event)
{
    if (pnlGrid->is_paused)
    {
        pnlGrid->advance_generation();
        show_message("Advanced one step...");
    }
    update_status_bar();
}


/// @brief wxEVT_TOOL or wxEVT_MENU handler for warp tool toggle button
/// @param event wxCommandEvent
void wxFrame_CGOL::on_click_warp(wxCommandEvent& event)
{
    if (event.GetId()==id_tool_warp_key)
    {
        bool is_warp = pnlGrid->toggle_warp();
        tbarMain->ToggleTool(id_tool_warp, is_warp);
    }
    else
    {
        pnlGrid->set_warp(tbarMain->GetToolState(id_tool_warp));
    }

    if (pnlGrid->get_warp())
        show_message("Let's do the time warp again...");
    else
        show_message("Let them disintegrate...");
}


/// @brief wxEVT_TOOL or wxEVT_MENU handler for grid tool toggle button
/// @param event wxCommandEvent
void wxFrame_CGOL::on_click_grid(wxCommandEvent& event)
{
    if (event.GetId()==id_tool_grid_key)
    {
        pnlGrid->is_grid_visible = !pnlGrid->is_grid_visible;
        tbarMain->ToggleTool(id_tool_grid, pnlGrid->is_grid_visible);
    }
    else
    {
        pnlGrid->is_grid_visible = tbarMain->GetToolState(id_tool_grid);
    }

    if (pnlGrid->is_grid_visible)
        show_message("Show the grid...");
    else
        show_message("Hide the grid...");

    if (pnlGrid->is_paused)
    {   // only need to do this if it is not currently running the game
        // if the game is running, it will redraw on the next step
        pnlGrid->redraw_grid();
        Refresh();
    }
}


/// @brief wxEVT_TOOL handler for slower tool button
/// @param event wxCommandEvent
void wxFrame_CGOL::on_click_slower(wxCommandEvent& event)
{
    int pos = sldSpeed->GetValue();
    pos = int(std::floor(double(pos)/AppConfig::SLIDER_CHG)*AppConfig::SLIDER_CHG) - AppConfig::SLIDER_CHG;
    if (pos < 0)
        pos = 0;
    sldSpeed->SetValue(pos);
    timer_period_ms = get_timer_ms(pos);
    is_reset_timer = true;
    if (pos == 0)
        show_message("At slowest speed...");
    else
        show_message("Slowed it down a notch...");
}


/// @brief wxEVT_TOOL handler for faster tool button
/// @param event wxCommandEvent
void wxFrame_CGOL::on_click_faster(wxCommandEvent& event)
{
    int pos = sldSpeed->GetValue();
    pos = int(std::ceil(double(pos)/AppConfig::SLIDER_CHG)*AppConfig::SLIDER_CHG) + AppConfig::SLIDER_CHG;
    if (pos > AppConfig::SLIDER_MAX)
        pos = AppConfig::SLIDER_MAX;
    sldSpeed->SetValue(pos);
    timer_period_ms = get_timer_ms(pos);
    is_reset_timer = true;
    if (pos == AppConfig::SLIDER_MAX)
        show_message("At fastest speed...");
    else
        show_message("Sped it up a notch...");
}


/// @brief wxEVT_TOOL handler for take snapshot tool button
/// @param event wxCommandEvent
void wxFrame_CGOL::on_click_snap(wxCommandEvent& event)
{
    CGOL_STRING snap = pnlGrid->take_snapshot();

    if (!snap.empty())
    {
        // copy snapshot to clipboard
        copy_text_to_clipboard(snap);
        show_message("Took snapshot of grid...");
    }
    else
    {
        show_message("Could not take snapshot of grid...");
    }
}


/// @brief Copy the text to the clipboard
/// @param clip text to copy to the clipboard
void wxFrame_CGOL::copy_text_to_clipboard(CGOL_STRING const& clip)
{
    if (wxTheClipboard->Open())
    {
        wxTheClipboard->Clear();
        wxTheClipboard->SetData(new wxTextDataObject(clip));
        wxTheClipboard->Flush();
        wxTheClipboard->Close();
    }
}


/// @brief Get text from the clipboard
/// @return text from the clipboard; "" if clipboard does not contain text
CGOL_STRING wxFrame_CGOL::get_text_from_clipboard()
{
    CGOL_STRING clip = wxEmptyString;

    if (wxTheClipboard->Open())
    {   if (wxTheClipboard->IsSupported(wxDF_TEXT))
        {
            wxTextDataObject data_object;
            if (wxTheClipboard->GetData(data_object))
                clip = data_object.GetText();
        }

        wxTheClipboard->Close();
    }

    return clip;
}


/// @brief wxEVT_TOOL handler for restore snapshot tool button
/// @param event wxCommandEvent
void wxFrame_CGOL::on_click_restore(wxCommandEvent& event)
{
    CGOL_STRING snap = get_text_from_clipboard();
    bool result = false;

    if (!snap.empty())
    {
        if (pnlGrid->restore_shapshot(snap))
        {
            pnlGrid->is_paused = true;
            register_rules();
            update_toolbar();
            update_status_bar();
            result = true;
        }
    }

    if (result)
        show_message("Restored snapshot to grid...");
    else
        show_message("Could not restore snapshot to grid...");
}


/// @brief wxEVT_TOOL handler for about tool button
/// @param event wxCommandEvent
void wxFrame_CGOL::on_click_about(wxCommandEvent& event)
{
    show_about_dialog();
}


/// @brief Sets the tool image for the given tool id
/// @param id id of the tool
/// @param bitmap bitmap of the image to set for the given tool
void wxFrame_CGOL::set_tool_image(int id, wxBitmap& bitmap)
{
    wxBitmapBundle bundle(bitmap);
    tbarMain->SetToolNormalBitmap(id, bundle);
}


/// @brief wxEVT_COMBOBOX handler for the game-select combo box
/// @param event wxCommandEvent
void wxFrame_CGOL::on_select_game(wxCommandEvent& event)
{
    pnlGrid->is_paused = true;
    int sel = cmbGame->GetSelection();
    if (sel >= N_ACTION_ITEMS)
        on_select_preset(sel-N_ACTION_ITEMS);
    else if (sel == NEW_GAME)
        on_new_game();
    else if (sel == LOAD_GAME)
        on_load_game();
    else if (sel == SAVE_GAME)
        on_save_game();

    if (!pnlGrid->name_of_game().empty())
    {
        CGOL_STRING msg;
        refresh_tool_and_status(msg);
    }
    else
    {
        refresh_tool_and_status();
    }

    refresh_games_list();
}


/// @brief Refresh and send size event with optional message
/// @param msg optional message; default="" -> no message
void wxFrame_CGOL::refresh_tool_and_status(CGOL_STRING const& msg)
{
    update_toolbar();
    update_status_bar();
    if (!msg.empty())
        show_message(msg);
    SendSizeEvent();
    Refresh();
}


/// @brief sub-handler called if a preset is selected in the combo box
/// @param preset index to the preset or registered game
void wxFrame_CGOL::on_select_preset(int preset)
{
    pnlGrid->load_preset(preset);
    register_rules(pnlGrid->get_rules());
    CGOL_STRING msg = CGOL_FORMAT("Loaded preset: %s", pnlGrid->name_of_game());
    show_message(msg);
}


/// @brief sub-handler called if new game is selected in the combo box
void wxFrame_CGOL::on_new_game()
{
    show_message("Creating new game...");
    dlgGetGridSize dlg(this);
    array_shape_t shape = pnlGrid->shape();
    int rows = shape.rows;
    int cols = shape.cols;
    dlg.set_spin_range(AppConfig::ROWS_MIN, AppConfig::ROWS_MAX, AppConfig::COLS_MIN, AppConfig::COLS_MAX);
    dlg.set_spin_values(rows, cols);

    dlg.SetTitle("New game: enter dimensions");
    if (dlg.ShowModal() == wxID_OK)
    {
        dlg.get_spin_values(rows, cols);
        pnlGrid->new_game({rows, cols});
        register_rules(pnlGrid->get_rules());
    }
}


/// @brief  sub-handler called if load game is selected in the combo box
void wxFrame_CGOL::on_load_game()
{
    show_message("Loading a game...");
    Designator result = pnlGrid->load_file();
    if (result)
    {   CGOL_STRING msg = CGOL_FORMAT("Loaded game: %s", result.name);
        show_message(msg);
        register_rules(pnlGrid->get_rules());
    }
}


/// @brief  sub-handler called if save game is selected in the combo box
void wxFrame_CGOL::on_save_game()
{
    show_message("Saving the game...");
    if (pnlGrid->save_file())
    {
        CGOL_STRING msg = CGOL_FORMAT("Saved game: %s", pnlGrid->name_of_game());
        refresh_games_list();
        show_message(msg);
    }
}


/// @brief Refresh the rules list and select the current rules set
void wxFrame_CGOL::refresh_rules_list()
{
    if (m_rules_list.empty())
    {
        m_rules_list = pnlGrid->get_rules_list();
    }
    RulesList rules_list = m_rules_list;
    Rules my_rules = pnlGrid->get_rules();
    rules_list.insert(rules_list.begin(), "(Edit rules)");
    cmbRules->Set(rules_list);
    cmbRules->SetStringSelection(my_rules);
}


/// @brief Refresh the games list and select the current game
void wxFrame_CGOL::refresh_games_list()
{
    GamesNamesList games_list = pnlGrid->get_games_names_list();
    CGOL_STRING name = pnlGrid->name_of_game();

    // find our game in the games list
    auto iter = std::find(games_list.begin(), games_list.end(), name);

    // this will give the index to the game if it exists, or the index one past
    // the end if it does not.
    size_t idx = std::distance(games_list.begin(), iter);

    // if the game was not in the list, add an entry at the end
    if (iter == games_list.end())
        games_list.push_back(UNSAVED_GAME);

    // now, prepend our action items (this must come after adding UNSAVED_GAME)
    games_list.insert(games_list.begin(), ACTION_ITEMS.begin(), ACTION_ITEMS.end());

    // now, set our full list and select our item
    cmbGame->Set(games_list);
    cmbGame->SetSelection(idx + N_ACTION_ITEMS);
}


/// @brief wxEVT_COMBOBOX handler for the rule-select combo box
/// @param event wxCommandEvent
void wxFrame_CGOL::on_select_rule(wxCommandEvent& event)
{
    pnlGrid->is_paused = true;

    int sel = cmbRules->GetSelection();

    if (sel==0)
    {   // edit rules
        on_click_status_rules();
    }
    else
    {   // choose a rule from the list
        CGOL_STRING rules = cmbRules->GetValue();
        pnlGrid->set_rules(rules);
        update_status_bar();
        update_toolbar();
        CGOL_STRING msg = CGOL_FORMAT("Rules: %s", rules);
        show_message(msg);
        Refresh();
    }
}


/// @brief wxEVT_SLIDER handler for the game-speed slider
/// @param event wxCommandEvent
void wxFrame_CGOL::on_scroll_speed(wxCommandEvent& event)
{
    int pos = sldSpeed->GetValue();
    timer_period_ms = get_timer_ms(pos);
    is_reset_timer = true;
}


/// @brief wxEVT_LEFT_DOWN handler for a click in the status bar
/// @param event wxMouseEvent
void wxFrame_CGOL::on_click_status(wxMouseEvent& event)
{
    wxPoint pos = event.GetPosition();
    int pos_x = pos.x;
    int idx_field = -1;
    wxRect rect;

    for (int idx=0; idx<STATUS_FIELD::N_FIELD_COUNT; ++idx)
    {
        stabStatusBar->GetFieldRect(idx, rect);
        if (rect.x <= pos_x && pos_x < (rect.x+rect.width))
        {
            idx_field = idx;
            break;
        }
    }

    switch (idx_field)
    {
        case STATUS_FIELD::STATE:
            on_click_status_state();
            break;
        case STATUS_FIELD::LIVE_COUNT:
            on_click_status_live();
            break;
        case STATUS_FIELD::GRID_SIZE:
            on_click_status_grid();
            break;
        case STATUS_FIELD::RULES_SET:
            on_click_status_rules();
            break;
        case STATUS_FIELD::MESSAGE:
            show_message("You clickedin the message area");
            break;
    }

    update_toolbar();
    update_status_bar();
    Refresh();
}


/// @brief sub-handler for a click in the status field of the status bar
void wxFrame_CGOL::on_click_status_state()
{
    if (pnlGrid->is_paused)
        show_message("Click the green triangle to play");
    else
        show_message("Click the yellow bars to pause");
}


/// @brief sub-handler for a click in the grid size field of the status bar
void wxFrame_CGOL::on_click_status_grid()
{
    pnlGrid->is_paused = true;
    show_message("Resizing grid...");
    dlgGetGridSize dlg(this);
    array_shape_t shape = pnlGrid->shape();
    int rows = shape.rows;
    int cols = shape.cols;
    dlg.set_spin_range(AppConfig::ROWS_MIN, AppConfig::ROWS_MAX, AppConfig::COLS_MIN, AppConfig::COLS_MAX);
    dlg.set_spin_values(rows, cols);
    dlg.SetTitle("Resize: enter dimensions");
    if (dlg.ShowModal() == wxID_OK)
    {
        int rows_gen;
        int cols_gen;
        dlg.get_spin_values(rows_gen, cols_gen);
        array_shape_t shape = {rows_gen, cols_gen};
        pnlGrid->resize_game(shape);
        shape = pnlGrid->shape();
        SendSizeEvent();
        CGOL_STRING msg = CGOL_FORMAT("Resized grid to %dx%d", shape.rows, shape.cols);
        show_message(msg);
    }
}


/// @brief sub-handler for a click in the rules field of the status bar
void wxFrame_CGOL::on_click_status_rules()
{
    pnlGrid->is_paused = true;
    RuleSpec spec;
    pnlGrid->get_rule_spec(spec);
    show_message("Changing the rules...");
    dlgEditRules dlg(this);
    dlg.set_rules(spec);

    if (dlg.ShowModal()==wxID_OK)
    {
        dlg.get_rules(spec);
        if (spec.birth.empty() || spec.survive.empty())
        {
            show_message("Invalid rules! No change made...");
        }
        else
        {
            pnlGrid->set_rule_spec(spec);
            Rules rules = pnlGrid->get_rules();
            register_rules(rules);
            CGOL_STRING msg = CGOL_FORMAT("Changed the rules to %s...", rules);
            show_message(msg);
        }
    }

    update_toolbar();
    update_status_bar();
    Refresh();
}


/// @brief Register the given rules with the game and select in the rules combo
/// @param rules rules in B/S format
void wxFrame_CGOL::register_rules(Rules rules)
{
    if (rules.empty())
        rules = pnlGrid->get_rules();

    // if rules is not in current rules list, add it
    GamesNamesList::iterator iter = std::find(m_rules_list.begin(), m_rules_list.end(), rules);

    if (iter==m_rules_list.end())
    {   // not on the list, add it
        m_rules_list.push_back(rules);
    }

    refresh_rules_list();
}


/// @brief sub-handler for a click in the live cell count field of the status bar
void wxFrame_CGOL::on_click_status_live()
{
    int live_cells = pnlGrid->get_live_cell_count();
    CGOL_STRING msg = CGOL_FORMAT("The live cell count is %d", live_cells);
    show_message(msg);
}


/// @brief Update the images and tool states for tools in the toolbar
void wxFrame_CGOL::update_toolbar()
{
    if (pnlGrid->is_paused)
    {
        set_tool_image(id_tool_play, bitmap_play);
        toolStep->Enable(true);
    }
    else
    {
        set_tool_image(id_tool_play, bitmap_pause);
        toolStep->Enable(false);
    }

    tbarMain->ToggleTool(id_tool_warp, pnlGrid->get_warp());
    tbarMain->ToggleTool(id_tool_grid, pnlGrid->is_grid_visible);

    tbarMain->Realize();
}


/// @brief Update the fields in the status bar
void wxFrame_CGOL::update_status_bar()
{
    CGOL_STRING str;

    if (pnlGrid->is_paused)
        stabStatusBar->SetStatusText("Paused", STATUS_FIELD::STATE);
    else
        stabStatusBar->SetStatusText("Running", STATUS_FIELD::STATE);

    int live_cells = pnlGrid->get_live_cell_count();
    str = CGOL_FORMAT("Live cells: %d", live_cells);
    stabStatusBar->SetStatusText(str, STATUS_FIELD::LIVE_COUNT);

    array_shape_t shape = pnlGrid->shape();
    str = CGOL_FORMAT("%d x %d", shape.rows, shape.cols);
    stabStatusBar->SetStatusText(str, STATUS_FIELD::GRID_SIZE);

    str = pnlGrid->get_rules();
    stabStatusBar->SetStatusText(str, STATUS_FIELD::RULES_SET);
}


/// @brief Event handler for the regular task timer
/// @param event wxTimerEvent
/// @note The regular task timer handles periodic and one-shot events such as
/// the momentary message display in the status bar.
void wxFrame_CGOL::on_task_timer(wxTimerEvent& event)
{
    if (ctr_message != 0)
    {
        if (--ctr_message == 0)
        {   // clear any existing message since it has timed out
            GetStatusBar()->SetStatusText(CGOL_EMPTY_STRING, STATUS_FIELD::MESSAGE);
        }
    }
}


/// @brief Event handler for the game timer
/// @param event wxTimerEvent
/// @note The game timer has a variable period, with the period depending upon
/// the selected game-speed. Game animation is controlled through this timer.
void wxFrame_CGOL::on_game_timer(wxTimerEvent& event)
{
    if (!pnlGrid->is_paused)
    {
        pnlGrid->advance_generation();
        update_status_bar();
    }

    if (is_reset_timer)
    {
        is_reset_timer = false;
        p_gameTimer->Start(timer_period_ms);
    }
}


/// @brief Show a brief message in the status bar
/// @param message Message to display
/// @param time_ms Time (in ms) to display the message. Default=0
/// @note If time_ms == 0, the configured application message time will be used.
void wxFrame_CGOL::show_message(CGOL_STRING const& message, int time_ms)
{
    if (!message.empty())
    {
        GetStatusBar()->SetStatusText(message, STATUS_FIELD::MESSAGE);
        if (time_ms == 0)
            time_ms = AppConfig::MESSAGE_DISPLAY_MS;
        ctr_message = time_ms / AppConfig::TASK_TICK_MS;
    }
    else
    {
        GetStatusBar()->SetStatusText(CGOL_EMPTY_STRING, STATUS_FIELD::MESSAGE);
        ctr_message = 0;
    }
}


/// @brief Calculate the slider position for the given game timer setting
/// @param timer_ms timer setting in ms
/// @return slider position from 0 to SLIDER_MAX
int wxFrame_CGOL::get_slider_pos(int timer_ms)
{
    double t_min = AppConfig::TIMER_MIN_MS;
    double t_max = AppConfig::TIMER_MAX_MS;
    double r_timer = t_max / t_min;
    double x = std::log(double(timer_ms) / t_min) / std::log(r_timer);
    int slider = AppConfig::SLIDER_MAX * (1.0 - x);
    return slider;
}


/// @brief Calculate the game timer period from the slider position
/// @param slider  slider position from 0 to SLIDER_MAX
/// @return timer setting in ms (from TIMER_MIN_MS to TIMER_MAX_MS)
int wxFrame_CGOL::get_timer_ms(int slider)
{
    double t_min = AppConfig::TIMER_MIN_MS;
    double t_max = AppConfig::TIMER_MAX_MS;
    double s_max    = AppConfig::SLIDER_MAX;
    double r_timer = t_max / t_min;
    int timer_ms = t_min * std::pow(r_timer, (s_max-slider)/s_max) + 0.5;
    if (timer_ms < AppConfig::TIMER_MIN_MS)
        timer_ms = AppConfig::TIMER_MIN_MS;
    else if (timer_ms > AppConfig::TIMER_MAX_MS)
        timer_ms = AppConfig::TIMER_MAX_MS;
    return timer_ms;
}


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/