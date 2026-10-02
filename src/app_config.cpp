/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : app_config.cpp
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file contains definitions of some configuration parameters for the game.
*
*  Change log:
*    2026-09-21  KSM  Created
*    2026-09-24  KSM  Moved standard types and preset games into this file
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#include "app_config.h"

const GamesList AppConfig::CGOL_GAME_PRESETS =
{
    { "Glider", 32, 32, true, "B3/S23", 0, "x.x;.xx;.x."},
    { "Beacon", 16, 16, true, "B3/S23", 0, "xx..;xx..;..xx;..xx"},
    { "Pulsar-3", 32, 32, true, "B3/S23", 0,
        "..xxx...xxx..;"
        ".............;"
        "x....x.x....x;"
        "x....x.x....x;"
        "x....x.x....x;"
        "..xxx...xxx..;"
        ".............;"
        "..xxx...xxx..;"
        "x....x.x....x;"
        "x....x.x....x;"
        "x....x.x....x;"
        ".............;"
        "..xxx...xxx.."
    },

    {
        "Spaceship LWSS", 16, 32, true, "B3/S23", 0,
        ".xxxx;"
        "x...x;"
        "....x;"
        "x..x."
    },

    {
        "Spaceship HWSS", 16, 32, true, "B3/S23", 0,
        ".xxxxxx;"
        "x.....x;"
        "......x;"
        "x....x.;"
        "..xx..."
    },

    { "Spaceship MWSS", 16, 32, true, "B3/S23", 0,
        "..x...;"
        "x...x.;"
        ".....x;"
        "x....x;"
        ".xxxxx"
    },

    {
        "Pentadecathlon-15", 48, 48, true, "B3/S23", 0,
        "xxx;"
        ".x.;"
        ".x.;"
        "xxx;"
        "...;"
        "xxx;"
        "xxx;"
        "...;"
        "xxx;"
        ".x.;"
        ".x.;"
        "xxx"
    },

    {
        "B-heptomino", 80, 80, false, "B3/S23", 0,
        "x.xx;"
        "xxx.;"
        ".x.."
    },

    {
        "I-heptomino", 80, 80, false, "B3/S23", 0,
        "..xx;"
        ".xx.;"
        ".x..;"
        "xx.."
    },

    {
        "R-pentomino", 120, 120, true, "B3/S23", 0,
        ".xx;"
        "xx.;"
        ".x."
    },

    {
        "Diehard", 48, 48, true, "B3/S23", 0,
        "......x.;"
        "xx......;"
        ".x...xxx"
    },

    {
        "Acorn", 80, 80, true, "B3/S23", 0,
        ".x.....;"
        "...x...;"
        "xx..xxx"
    },

    {
        "Gosper glider gun", 64, 64, false, "B3/S23", 0,
        "........................x...........;"
        "......................x.x...........;"
        "............xx......xx............xx;"
        "...........x...x....xx............xx;"
        "xx........x.....x...xx..............;"
        "xx........x...x.xx....x.x...........;"
        "..........x.....x.......x...........;"
        "...........x...x....................;"
        "............xx......................"
    },

    {
        "Simkin glider gun", 80, 80, false, "B3/S23", 0,
        "xx.....xx........................;"
        "xx.....xx........................;"
        ".................................;"
        "....xx...........................;"
        "....xx...........................;"
        ".................................;"
        ".................................;"
        ".................................;"
        ".................................;"
        "......................xx.xx......;"
        ".....................x.....x.....;"
        ".....................x......x..xx;"
        ".....................xxx...x...xx;"
        "..........................x......;"
        ".................................;"
        ".................................;"
        ".................................;"
        "....................xx...........;"
        "....................x............;"
        ".....................xxx.........;"
        ".......................x........."
    },


    { "Puffer train", 128, 128, false, "B3/S23", 7,
        ".xxx...........xxx;"
        "x..x..........x..x;"
        "...x....xxx......x;"
        "...x....x..x.....x;"
        "..x....x........x.;"
        "..................;"
        "..................;"
        "..................;"
        ".................."
    },

    // Twinkle twinkle contributed by Lorna Martin 2026-09-30
    { "Twinkle twinkle", 80, 80, true, "B3/S23", 0,
        "..x.......................x..;"
        "xx.xx...................xx.xx;"
        "..x.......................x..;"
        ".............................;"
        ".............................;"
        "...........x..x..x...........;"
        "..........x.x...x.x..........;"
        "...........xx.x.xx...........;"
        ".............x.x.............;"
        "..........x.x...x.x..........;"
        ".............x.x.............;"
        "...........xx.x.xx...........;"
        "..........x.x...x.x..........;"
        "...........x..x..x...........;"
        ".............................;"
        ".............................;"
        ".............................;"
        ".............................;"
        "...x.....................x...;"
        ".xx.xx.................xx.xx.;"
        "...x.....................x..."
    }
};


/// @brief Vector containing entries for the context-menu
/// @note
const StructureList AppConfig::CGOL_CONTEXT_LIST =
{
    // label entries: return value is entry.head.c
    //{ "Clear grid", "", {-1,0} },
    StructureSpec::LABEL("Clear grid", 0),

    StructureSpec::SEPARATOR,

    // Structure pattern entries
    StructureSpec::PATTERN( "Glider", "x.x;.xx;.x.", {2,2} ),
    { "Beacon", "xx..;xx..;..xx;..xx", {1,1} },
    { "Blinker", "xxx", {0,1} },
    { "Block", "xx;xx", {0,0} },
    { "Beehive", ".xx.;x..x;.xx.", {1,1} },
    { "Tub", ".x.;x.x;.x.", {1,1} },
    { "Toad", ".xxx;xxx.", {0,1} },
    { "Bowtie", ".xx;x.x;xx.", {1,1} },
    { "LWSS", ".xxxx;x...x;....x;x..x.", {1,4} },
    { "MWSS", "..x...;x...x.;.....x;x....x;.xxxxx", {2,5} },
    { "HWSS", ".xxxxxx;x.....x;......x;x....x.;..xx...", {2,6} }
};


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/