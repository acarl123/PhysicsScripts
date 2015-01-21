# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class genericView ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_menubar1 = wx.MenuBar( 0 )
		self.menuFile = wx.Menu()
		self.menuLoad = wx.MenuItem( self.menuFile, wx.ID_ANY, u"&Load Module...", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuLoad )

		self.menuExit = wx.MenuItem( self.menuFile, wx.ID_ANY, u"&Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuExit )

		self.m_menubar1.Append( self.menuFile, u"&File" )

		self.SetMenuBar( self.m_menubar1 )


		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


