/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : cgol_images.h
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file defines the encoded bitmaps for icons and tool images.
*
*  Change log:
*    2026-09-21  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#pragma once

#include <wx/bitmap.h>
#include <wx/icon.h>

// helper functions to make loading these images easier
wxBitmap get_bitmap(unsigned char const bitmap[], size_t length);
wxIcon   get_icon(unsigned char const bitmap[], size_t length);

unsigned char CGOL_game_icon_16x16[];
#define LEN_CGOL_game_icon_16x16 2276

unsigned char CGOL_game_icon_24x24[];
#define LEN_CGOL_game_icon_24x24 2358

unsigned char CGOL_game_icon_32x32[];
#define LEN_CGOL_game_icon_32x32 2395

unsigned char CGOL_game_icon_48x48[];
#define LEN_CGOL_game_icon_48x48 2473

unsigned char CGOL_game_icon_128x128[];
#define LEN_CGOL_game_icon_128x128 2786

unsigned char CGOL_game_icon_256x256[];
#define LEN_CGOL_game_icon_256x256 3305

unsigned char image_play[];
#define LEN_IMAGE_PLAY 2327

unsigned char image_pause[];
#define LEN_IMAGE_PAUSE 2216

unsigned char image_step[];
#define LEN_IMAGE_STEP 2373

unsigned char image_warp[];
#define LEN_IMAGE_WARP 3226

unsigned char image_grid[];
#define LEN_IMAGE_GRID 2363

unsigned char image_faster[];
#define LEN_IMAGE_FASTER 2183

unsigned char image_slower[];
#define LEN_IMAGE_SLOWER 2199

unsigned char image_snap[];
#define LEN_IMAGE_SNAP 3310

unsigned char image_restore[];
#define LEN_IMAGE_RESTORE 3377

unsigned char image_about[];
#define LEN_IMAGE_ABOUT 3091


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/