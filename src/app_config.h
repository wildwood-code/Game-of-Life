/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : app_config.h
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file contains declarations of configuration parameters for the game.
*
*  Change log:
*    2026-09-21  KSM  Created
*    2026-09-24  KSM  Moved standard types and preset games into this file
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#pragma once

#include "cgol_types.h"


namespace AppConfig
{
    // version information
    ////// inline constexpr char VERSION[] = "1.0";

    // game settings
    inline constexpr int INITIAL_GAME_INDEX = 0;

    // timer properties
    inline constexpr int TIMER_MIN_MS = 20;
    inline constexpr int TIMER_MAX_MS = 200;
    inline constexpr int TIMER_INI_MS = 50;

    // message display properties
    inline constexpr int MESSAGE_DISPLAY_MS = 2000;
    inline constexpr int TASK_TICK_MS = 50;

    // timer slider properties
    inline constexpr int SLIDER_MAX = 100;  // max value of slider (min will be 0)
    inline constexpr int SLIDER_CHG = 10;   // timer increment via buttons

    // color settings:  NOTE: COLORS ARE ORDERED BLUE GREEN RED
    //                                             BB'GG'RR
    inline constexpr uint32_t BACKGROUND_COLOR = 0xF0'F0'F0;
    inline constexpr uint32_t LIVE_CELL_COLOR  = 0x00'00'00;
    inline constexpr uint32_t HIGHLIGHT_COLOR  = 0x00'FF'00;
    inline constexpr uint32_t GRID_COLOR       = 0xDC'DC'DC;

    // grid settings
    inline constexpr int CELL_W = 12;
    inline constexpr int CELL_H = 12;
    inline constexpr int ROWS_MIN = 8;
    inline constexpr int ROWS_MAX = 256;
    inline constexpr int COLS_MIN = 8;
    inline constexpr int COLS_MAX = 256;

    // new-game default size
    inline constexpr int ROWS_NEW_GAME = 16;
    inline constexpr int COLS_NEW_GAME = 16;

    // pre-defined CGOL game declaration (definition is in AppConfig.cpp)
    extern const GamesList CGOL_GAME_PRESETS;

    // pre-defined context-menu list
    extern const StructureList CGOL_CONTEXT_LIST;
}


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/