import wx
import os, sys

from genericView import genericView


class mainController:
   def __init__(self):
      # init member vars
      self.mainWindow = genericView(None)

      # setup bindings
      self.mainWindow.Bind(wx.EVT_MENU, self.onExit, self.mainWindow.menuExit)
      self.mainWindow.Bind(wx.EVT_MENU, self.onLoad, self.mainWindow.menuLoad)

   def show(self):
      self.mainWindow.Show()

   def onExit(self, event):
      exit(0)

   def onLoad(self, event):
      dlg = wx.FileDialog
      wx.simple