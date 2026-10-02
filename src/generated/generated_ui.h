///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
// http://www.wxformbuilder.org/
//
// PLEASE DO *NOT* EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#pragma once

#include <wx/artprov.h>
#include <wx/xrc/xmlres.h>
class wxPanel_Grid;

#include <wx/string.h>
#include <wx/bitmap.h>
#include <wx/image.h>
#include <wx/icon.h>
#include <wx/combobox.h>
#include <wx/gdicmn.h>
#include <wx/font.h>
#include <wx/colour.h>
#include <wx/settings.h>
#include <wx/slider.h>
#include <wx/toolbar.h>
#include <wx/panel.h>
#include <wx/sizer.h>
#include <wx/statusbr.h>
#include <wx/frame.h>

///////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
/// Class wxFrame_Main
///////////////////////////////////////////////////////////////////////////////
class wxFrame_Main : public wxFrame
{
	private:

	protected:
		wxToolBar* tbarMain;
		wxToolBarToolBase* toolPlay;
		wxToolBarToolBase* toolStep;
		wxComboBox* cmbGame;
		wxComboBox* cmbRules;
		wxToolBarToolBase* toolWarp;
		wxToolBarToolBase* toolGrid;
		wxToolBarToolBase* toolTakeSnap;
		wxToolBarToolBase* toolRestoreSnap;
		wxToolBarToolBase* toolSlower;
		wxSlider* sldSpeed;
		wxToolBarToolBase* toolFaster;
		wxToolBarToolBase* toolAbout;
		wxPanel_Grid* pnlGrid;
		wxStatusBar* stabStatusBar;

	public:
		wxBoxSizer* szrMain;
		wxBoxSizer* szrSub;

		wxFrame_Main( wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = wxT("Conway's Game of Life"), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxSize( 936,549 ), long style = wxCAPTION|wxCLOSE_BOX|wxRESIZE_BORDER|wxSYSTEM_MENU );

		~wxFrame_Main();

};

