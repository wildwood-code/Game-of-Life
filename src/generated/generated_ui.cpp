///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
// http://www.wxformbuilder.org/
//
// PLEASE DO *NOT* EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#include "../panel_grid.h"

#include "generated_ui.h"

///////////////////////////////////////////////////////////////////////////

wxFrame_Main::wxFrame_Main( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxFrame( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxSize( 800,480 ), wxDefaultSize );

	tbarMain = this->CreateToolBar( wxTB_HORIZONTAL, wxID_ANY );
	tbarMain->SetToolBitmapSize( wxSize( 48,48 ) );
	toolPlay = tbarMain->AddTool( wxID_ANY, wxT("Play/pause"), wxArtProvider::GetBitmap( wxASCII_STR(wxART_TIP), wxASCII_STR(wxART_TOOLBAR) ), wxNullBitmap, wxITEM_NORMAL, wxT("Play/pause"), wxT("Play/pause"), NULL );

	toolStep = tbarMain->AddTool( wxID_ANY, wxT("Single step"), wxArtProvider::GetBitmap( wxASCII_STR(wxART_TIP), wxASCII_STR(wxART_TOOLBAR) ), wxNullBitmap, wxITEM_NORMAL, wxT("Single step"), wxT("Single step"), NULL );

	tbarMain->AddSeparator();

	cmbGame = new wxComboBox( tbarMain, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0, NULL, wxCB_READONLY );
	cmbGame->Append( wxT("<add games here>") );
	cmbGame->SetSelection( 0 );
	cmbGame->SetToolTip( wxT("Select game") );

	tbarMain->AddControl( cmbGame );
	tbarMain->AddSeparator();

	cmbRules = new wxComboBox( tbarMain, wxID_ANY, wxT("Combo!"), wxDefaultPosition, wxSize( 100,-1 ), 0, NULL, wxCB_READONLY );
	cmbRules->Append( wxT("B3/S23") );
	cmbRules->SetSelection( 0 );
	cmbRules->SetToolTip( wxT("Select rules") );
	cmbRules->SetMinSize( wxSize( 100,-1 ) );

	tbarMain->AddControl( cmbRules );
	tbarMain->AddSeparator();

	toolWarp = tbarMain->AddTool( wxID_ANY, wxT("Warp"), wxArtProvider::GetBitmap( wxASCII_STR(wxART_TIP), wxASCII_STR(wxART_TOOLBAR) ), wxNullBitmap, wxITEM_CHECK, wxT("Warp at edge"), wxEmptyString, NULL );

	toolGrid = tbarMain->AddTool( wxID_ANY, wxT("Grid"), wxArtProvider::GetBitmap( wxASCII_STR(wxART_TIP), wxASCII_STR(wxART_TOOLBAR) ), wxNullBitmap, wxITEM_CHECK, wxEmptyString, wxEmptyString, NULL );

	tbarMain->AddSeparator();

	toolTakeSnap = tbarMain->AddTool( wxID_ANY, wxT("Take snapshot"), wxArtProvider::GetBitmap( wxASCII_STR(wxART_TIP), wxASCII_STR(wxART_TOOLBAR) ), wxNullBitmap, wxITEM_NORMAL, wxT("Take snapshot"), wxT("Take snapshot"), NULL );

	toolRestoreSnap = tbarMain->AddTool( wxID_ANY, wxT("Restore snapshot"), wxArtProvider::GetBitmap( wxASCII_STR(wxART_TIP), wxASCII_STR(wxART_TOOLBAR) ), wxNullBitmap, wxITEM_NORMAL, wxT("Restore snapshot"), wxT("Restore snapshot"), NULL );

	tbarMain->AddSeparator();

	toolSlower = tbarMain->AddTool( wxID_ANY, wxT("Slower"), wxArtProvider::GetBitmap( wxASCII_STR(wxART_TIP), wxASCII_STR(wxART_TOOLBAR) ), wxNullBitmap, wxITEM_NORMAL, wxT("Slower"), wxT("Slower"), NULL );

	sldSpeed = new wxSlider( tbarMain, wxID_ANY, 50, 0, 100, wxDefaultPosition, wxDefaultSize, wxSL_HORIZONTAL );
	sldSpeed->SetToolTip( wxT("Game speed") );

	tbarMain->AddControl( sldSpeed );
	toolFaster = tbarMain->AddTool( wxID_ANY, wxT("Faster"), wxArtProvider::GetBitmap( wxASCII_STR(wxART_TIP), wxASCII_STR(wxART_TOOLBAR) ), wxNullBitmap, wxITEM_NORMAL, wxT("Faster"), wxT("Faster"), NULL );

	tbarMain->AddSeparator();

	toolAbout = tbarMain->AddTool( wxID_ANY, wxT("About"), wxArtProvider::GetBitmap( wxASCII_STR(wxART_TIP), wxASCII_STR(wxART_TOOLBAR) ), wxNullBitmap, wxITEM_NORMAL, wxT("About"), wxT("About"), NULL );

	tbarMain->Realize();

	szrMain = new wxBoxSizer( wxVERTICAL );


	szrMain->Add( 0, 0, 1, wxEXPAND, 0 );

	szrSub = new wxBoxSizer( wxHORIZONTAL );


	szrSub->Add( 0, 0, 1, wxEXPAND, 0 );

	pnlGrid = new wxPanel_Grid( this, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxBORDER_SIMPLE|wxFULL_REPAINT_ON_RESIZE );
	pnlGrid->SetBackgroundColour( wxSystemSettings::GetColour( wxSYS_COLOUR_3DLIGHT ) );
	pnlGrid->SetMinSize( wxSize( 240,240 ) );

	szrSub->Add( pnlGrid, 0, wxALL|wxEXPAND, 0 );


	szrSub->Add( 0, 0, 1, wxEXPAND, 0 );


	szrMain->Add( szrSub, 0, wxEXPAND, 0 );


	szrMain->Add( 0, 0, 1, wxEXPAND, 0 );


	this->SetSizer( szrMain );
	this->Layout();
	stabStatusBar = this->CreateStatusBar( 5, wxSTB_SIZEGRIP, wxID_ANY );

	this->Centre( wxBOTH );
}

wxFrame_Main::~wxFrame_Main()
{
}
