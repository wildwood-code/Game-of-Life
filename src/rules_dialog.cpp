/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : rules_dialog.cpp
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file implents the dialog box to edit rules.
*
*  Change log:
*    2026-09-28  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#include "rules_dialog.h"


// number of neighboring cells. this will always be 8 for a square grid
#define N_NEIGHBOR_CELLS 8


/// @brief dlgEditRules constructor
/// @param parent  parent window of the dialog box
/// @param id     default=wxID_ANY
/// @param title  dialog title; default="Rules editor"
/// @param pos    default=wxDefaultPosition
/// @param size   default=wxDefaultSize
/// @param style  default=wxDEFAULT_DIALOG_STYLE
dlgEditRules::dlgEditRules( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style )
: wxDialog( parent, id, title, pos, size, style )
{
    m_spec = RuleSpec();

	this->SetSizeHints( wxDefaultSize, wxDefaultSize );

	wxBoxSizer* bSizer_h_rules;
	bSizer_h_rules = new wxBoxSizer( wxHORIZONTAL );
	bSizer_h_rules->Add( 20, 0, 0, wxEXPAND, 5 );

	wxBoxSizer* bSizer_v_rules;
	bSizer_v_rules = new wxBoxSizer( wxVERTICAL );
	bSizer_v_rules->Add( 0, 20, 0, wxEXPAND, 5 );

	wxFlexGridSizer* fgSizer_rules;
	fgSizer_rules = new wxFlexGridSizer( 0, 9, 0, 0 );
	fgSizer_rules->SetFlexibleDirection( wxBOTH );
	fgSizer_rules->SetNonFlexibleGrowMode( wxFLEX_GROWMODE_SPECIFIED );

	m_staticText_corner = new wxStaticText( this, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_corner->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_corner, 0, wxALL, 5 );

	m_staticText_1 = new wxStaticText( this, wxID_ANY, wxT("1"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_1->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_1, 0, wxALL, 5 );

	m_staticText_2 = new wxStaticText( this, wxID_ANY, wxT("2"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_2->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_2, 0, wxALL, 5 );

	m_staticText_3 = new wxStaticText( this, wxID_ANY, wxT("3"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_3->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_3, 0, wxALL, 5 );

	m_staticText_4 = new wxStaticText( this, wxID_ANY, wxT("4"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_4->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_4, 0, wxALL, 5 );

	m_staticText_5 = new wxStaticText( this, wxID_ANY, wxT("5"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_5->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_5, 0, wxALL, 5 );

	m_staticText_6 = new wxStaticText( this, wxID_ANY, wxT("6"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_6->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_6, 0, wxALL, 5 );

	m_staticText_7 = new wxStaticText( this, wxID_ANY, wxT("7"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_7->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_7, 0, wxALL, 5 );

	m_staticText_8 = new wxStaticText( this, wxID_ANY, wxT("8"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_8->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_8, 0, wxALL, 5 );

	m_staticText_birth = new wxStaticText( this, wxID_ANY, wxT("B:"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_birth->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_birth, 0, wxALL, 5 );

    m_birth_checks = new wxCheckBox*[N_NEIGHBOR_CELLS];
    m_survive_checks = new wxCheckBox*[N_NEIGHBOR_CELLS];

    for (int i=0; i<N_NEIGHBOR_CELLS; ++i)
    {
        m_birth_checks[i] = new wxCheckBox(this, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0);
        fgSizer_rules->Add(m_birth_checks[i], 0, wxALL, 5);
    }

	m_staticText_survive = new wxStaticText( this, wxID_ANY, wxT("S:"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText_survive->Wrap( -1 );
	fgSizer_rules->Add( m_staticText_survive, 0, wxALL, 5 );

    for (int i=0; i<N_NEIGHBOR_CELLS; ++i)
    {
        m_survive_checks[i] = new wxCheckBox(this, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0);
        fgSizer_rules->Add(m_survive_checks[i], 0, wxALL, 5);
    }

	bSizer_v_rules->Add( fgSizer_rules, 1, wxEXPAND, 5 );

	bSizer_v_rules->Add( 0, 20, 0, wxEXPAND, 5 );

	m_sdbSizer_rules = new wxStdDialogButtonSizer();
	m_sdbSizer_rules_OK = new wxButton( this, wxID_OK );
	m_sdbSizer_rules->AddButton( m_sdbSizer_rules_OK );
	m_sdbSizer_rules_Cancel = new wxButton( this, wxID_CANCEL );
	m_sdbSizer_rules->AddButton( m_sdbSizer_rules_Cancel );
    m_sdbSizer_rules_OK->SetDefault();
	m_sdbSizer_rules->Realize();

	bSizer_v_rules->Add( m_sdbSizer_rules, 0, wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 5 );
	bSizer_v_rules->Add( 0, 20, 0, wxEXPAND, 5 );
	bSizer_h_rules->Add( bSizer_v_rules, 1, wxEXPAND, 5 );
	bSizer_h_rules->Add( 20, 0, 0, wxEXPAND, 5 );

	this->SetSizer( bSizer_h_rules );
	this->Layout();
	bSizer_h_rules->Fit( this );

	this->Centre( wxBOTH );
}


/// @brief dlgEditRules destructor
dlgEditRules::~dlgEditRules()
{
    delete [] m_birth_checks;
    delete [] m_survive_checks;
}


/// @brief Set dialog checkboxes from the given rule spec
/// @param spec
void dlgEditRules::set_rules(const RuleSpec& spec)
{
    for (int i=0; i<8; ++i)
    {
        int cells = i+1;
        m_birth_checks[i]->SetValue(spec.birth.contains(cells));
        m_survive_checks[i]->SetValue(spec.survive.contains(cells));
    }
}


/// @brief Get dialog checkbox states into the given rule spec
/// @param spec
void dlgEditRules::get_rules(RuleSpec& spec)
{
    spec.birth.clear();
    spec.survive.clear();
    for (int i=0; i<8; ++i)
    {
        int cells = i+1;
        if (m_birth_checks[i]->GetValue())
            spec.birth.insert(cells);
        if (m_survive_checks[i]->GetValue())
            spec.survive.insert(cells);
    }
}


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/