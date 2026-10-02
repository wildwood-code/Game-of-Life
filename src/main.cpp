/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : main.cpp
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file is the primary app entry point.
*
*    The GUI is designed using wxFormBuilder and generated as wxWidgets code.
*
*  Change log:
*    2026-09-20  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************
* TODO: Feature and bug-fix request
*  Light/dark themes?
* ******************************************************************************/

#include "app_config.h"
#include <wx/wx.h>
#include "cgol_frame.h"


class wxApp_CGOL : public wxApp {

public:
    virtual bool OnInit() {

        CGOL_STRING filename = CGOL_EMPTY_STRING;
        wxFrame_CGOL* frame;

        if ( this->argc > 1 )
            filename = this->argv[1];

        wxInitAllImageHandlers();

        frame = new wxFrame_CGOL(filename);
        frame->Show(true);

        return true;
    }
};


wxIMPLEMENT_APP(wxApp_CGOL);


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/