/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : size_dialog.h
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file defines the interface for the grid size dialog box.
*
*  Change log:
*    2026-09-29  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#pragma once

#include <wx/stattext.h>
#include <wx/spinctrl.h>
#include <wx/button.h>
#include <wx/dialog.h>


class dlgGetGridSize : public wxDialog
{
	private:

	protected:
		wxStaticText* m_staticText2;
		wxStaticText* m_staticText4;
		wxSpinCtrl* spinRows;
		wxSpinCtrl* spinCols;
		wxStdDialogButtonSizer* sdbSizerButtons;
		wxButton* sdbSizerButtonsOK;
		wxButton* sdbSizerButtonsCancel;

    public:
		dlgGetGridSize( wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = wxT("Enter grid dimensions"), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxDefaultSize, long style = wxDEFAULT_DIALOG_STYLE );
		~dlgGetGridSize();

        void set_spin_range(int min_r, int max_r, int min_c, int max_c);
        void set_spin_values(int rows, int cols);
        void get_spin_values(int& rows, int& cols);

        /// @brief Set both the rows and cols spin controls to the same range
        /// @param min
        /// @param max
        void set_spin_range(int min, int max)
        {   // set both rows and cols to the same ranges
            set_spin_range(min, max, min, max);
        }
};


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/