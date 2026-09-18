# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from app.cgol_game_grid import pnlGameGrid
import wx
import wx.xrc

###########################################################################
## Class frmMain
###########################################################################

class frmMain ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Conway's Game of Life", pos = wx.DefaultPosition, size = wx.Size( 936,549 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU )

        self.SetSizeHints( wx.Size( 800,480 ), wx.DefaultSize )

        self.tbarMain = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
        self.tbarMain.SetToolBitmapSize( wx.Size( 48,48 ) )
        self.toolPlay = self.tbarMain.AddTool( wx.ID_ANY, u"Play/pause", wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Play/pause", u"Play/pause", None )

        self.toolStep = self.tbarMain.AddTool( wx.ID_ANY, u"Single step", wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Single step", u"Single step", None )

        self.tbarMain.AddSeparator()

        cmbGameChoices = [ u"<add games here>" ]
        self.cmbGame = wx.ComboBox( self.tbarMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cmbGameChoices, wx.CB_READONLY )
        self.cmbGame.SetSelection( 0 )
        self.cmbGame.SetToolTip( u"Select game" )

        self.tbarMain.AddControl( self.cmbGame )
        self.tbarMain.AddSeparator()

        cmbRulesChoices = [ u"B3/S23" ]
        self.cmbRules = wx.ComboBox( self.tbarMain, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.Size( 100,-1 ), cmbRulesChoices, wx.CB_READONLY )
        self.cmbRules.SetSelection( 0 )
        self.cmbRules.SetToolTip( u"Select rules" )
        self.cmbRules.SetMinSize( wx.Size( 100,-1 ) )

        self.tbarMain.AddControl( self.cmbRules )
        self.tbarMain.AddSeparator()

        self.toolWarp = self.tbarMain.AddTool( wx.ID_ANY, u"Warp", wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_CHECK, u"Warp at edge", wx.EmptyString, None )

        self.toolGrid = self.tbarMain.AddTool( wx.ID_ANY, u"Grid", wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

        self.tbarMain.AddSeparator()

        self.toolTakeSnap = self.tbarMain.AddTool( wx.ID_ANY, u"Take snapshot", wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Take snapshot", u"Take snapshot", None )

        self.toolRestoreSnap = self.tbarMain.AddTool( wx.ID_ANY, u"Restore snapshot", wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Restore snapshot", u"Restore snapshot", None )

        self.tbarMain.AddSeparator()

        self.toolSlower = self.tbarMain.AddTool( wx.ID_ANY, u"Slower", wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Slower", u"Slower", None )

        self.sldSpeed = wx.Slider( self.tbarMain, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        self.sldSpeed.SetToolTip( u"Game speed" )

        self.tbarMain.AddControl( self.sldSpeed )
        self.toolFaster = self.tbarMain.AddTool( wx.ID_ANY, u"Faster", wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Faster", u"Faster", None )

        self.tbarMain.AddSeparator()

        self.toolAbout = self.tbarMain.AddTool( wx.ID_ANY, u"About", wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"About", u"About", None )

        self.tbarMain.Realize()

        self.tmrGame = wx.Timer()
        self.tmrGame.SetOwner( self, self.tmrGame.GetId() )
        szrMain = wx.BoxSizer( wx.HORIZONTAL )


        szrMain.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.pnlGrid = pnlGameGrid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SIMPLE|wx.FULL_REPAINT_ON_RESIZE )
        self.pnlGrid.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        self.pnlGrid.SetMinSize( wx.Size( 240,240 ) )

        szrMain.Add( self.pnlGrid, 0, wx.EXPAND |wx.ALL, 5 )


        szrMain.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        self.SetSizer( szrMain )
        self.Layout()
        self.stabStatusBar = self.CreateStatusBar( 5, wx.STB_SIZEGRIP, wx.ID_ANY )

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


###########################################################################
## Class dlgGetDims
###########################################################################

class dlgGetDims ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Enter grid dimensions", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        gSizer1 = wx.GridSizer( 2, 2, 0, 0 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Rows", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        gSizer1.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.spinRows = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 8, 128, 16 )
        gSizer1.Add( self.spinRows, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Cols", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        gSizer1.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.spinCols = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 8, 128, 16 )
        gSizer1.Add( self.spinCols, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer2.Add( gSizer1, 1, wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        m_sdbSizerButtons = wx.StdDialogButtonSizer()
        self.m_sdbSizerButtonsOK = wx.Button( self, wx.ID_OK )
        m_sdbSizerButtons.AddButton( self.m_sdbSizerButtonsOK )
        self.m_sdbSizerButtonsCancel = wx.Button( self, wx.ID_CANCEL )
        m_sdbSizerButtons.AddButton( self.m_sdbSizerButtonsCancel )
        m_sdbSizerButtons.Realize()

        bSizer3.Add( m_sdbSizerButtons, 1, wx.EXPAND, 5 )


        bSizer2.Add( bSizer3, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer2 )
        self.Layout()
        bSizer2.Fit( self )

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


