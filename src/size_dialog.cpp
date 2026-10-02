/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : size_dialog.cpp
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file implements the grid size dialog box.
*
*  Change log:
*    2026-09-29  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#include "size_dialog.h"
#include <wx/sizer.h>


/// @brief Constructor for the grid size dialog
/// @param parent
/// @param id
/// @param title
/// @param pos
/// @param size
/// @param style
dlgGetGridSize::dlgGetGridSize( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxDialog( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxDefaultSize, wxDefaultSize );

	wxBoxSizer* bSizer2;
	bSizer2 = new wxBoxSizer( wxVERTICAL );

	wxGridSizer* gSizer1;
	gSizer1 = new wxGridSizer( 2, 2, 0, 0 );

	m_staticText2 = new wxStaticText( this, wxID_ANY, wxT("Rows"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText2->Wrap( -1 );
	gSizer1->Add( m_staticText2, 0, wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5 );

	spinRows = new wxSpinCtrl( this, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, wxSP_ARROW_KEYS, 8, 256, 16 );
	gSizer1->Add( spinRows, 0, wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5 );

	m_staticText4 = new wxStaticText( this, wxID_ANY, wxT("Cols"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText4->Wrap( -1 );
	gSizer1->Add( m_staticText4, 0, wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5 );

	spinCols = new wxSpinCtrl( this, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, wxSP_ARROW_KEYS, 8, 256, 16 );
	gSizer1->Add( spinCols, 0, wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5 );
	bSizer2->Add( gSizer1, 1, wxEXPAND, 5 );

	wxBoxSizer* bSizer3;
	bSizer3 = new wxBoxSizer( wxHORIZONTAL );

	sdbSizerButtons = new wxStdDialogButtonSizer();
	sdbSizerButtonsOK = new wxButton( this, wxID_OK );
	sdbSizerButtons->AddButton( sdbSizerButtonsOK );
	sdbSizerButtonsCancel = new wxButton( this, wxID_CANCEL );
	sdbSizerButtons->AddButton( sdbSizerButtonsCancel );
	sdbSizerButtons->Realize();
    sdbSizerButtonsOK->SetDefault();

	bSizer3->Add( sdbSizerButtons, 1, wxEXPAND, 5 );
	bSizer2->Add( bSizer3, 1, wxEXPAND, 5 );

	this->SetSizer( bSizer2 );
	this->Layout();
	bSizer2->Fit( this );

	this->Centre( wxBOTH );
}


/// @brief Destructor for the grid size dialog
dlgGetGridSize::~dlgGetGridSize()
{
}


/// @brief Set the range for the rows and cols spin controls
/// @param min_r
/// @param max_r
/// @param min_c
/// @param max_c
void dlgGetGridSize::set_spin_range(int min_r, int max_r, int min_c, int max_c)
{
    spinRows->SetRange(min_r, max_r);
    spinCols->SetRange(min_c, max_c);
}


/// @brief Set the current value for the rows and cols spin controls
/// @param rows
/// @param cols
void dlgGetGridSize::set_spin_values(int rows, int cols)
{
    spinRows->SetValue(rows);
    spinCols->SetValue(cols);
}


/// @brief Get the current value of the rows and cols spin controls
/// @param rows
/// @param cols
void dlgGetGridSize::get_spin_values(int& rows, int& cols)
{
    rows = spinRows->GetValue();
    cols = spinCols->GetValue();
}


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/