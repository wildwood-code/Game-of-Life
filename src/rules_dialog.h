/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : rules_dialog.h
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file defines the interface for the dialog box to edit rules.
*
*  Change log:
*    2026-09-28  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#pragma once

#include <wx/string.h>
#include <wx/stattext.h>
#include <wx/checkbox.h>
#include <wx/sizer.h>
#include <wx/button.h>
#include <wx/dialog.h>
#include "cgol_types.h"

class dlgEditRules : public wxDialog
{
	private:
        RuleSpec m_spec;

	protected:
		wxStaticText* m_staticText_corner;
		wxStaticText* m_staticText_1;
		wxStaticText* m_staticText_2;
		wxStaticText* m_staticText_3;
		wxStaticText* m_staticText_4;
		wxStaticText* m_staticText_5;
		wxStaticText* m_staticText_6;
		wxStaticText* m_staticText_7;
		wxStaticText* m_staticText_8;
		wxStaticText* m_staticText_birth;
		wxStaticText* m_staticText_survive;
        wxCheckBox** m_birth_checks;
        wxCheckBox** m_survive_checks;
		wxStdDialogButtonSizer* m_sdbSizer_rules;
		wxButton* m_sdbSizer_rules_OK;
		wxButton* m_sdbSizer_rules_Cancel;

	public:

		dlgEditRules( wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = wxT("Rules editor"), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxDefaultSize, long style = wxDEFAULT_DIALOG_STYLE );
        void set_rules(const RuleSpec& spec);
        void get_rules(RuleSpec& spec);

		~dlgEditRules();
};


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/