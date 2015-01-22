import string
import wx
import os, sys
import re

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
      dlg = wx.FileDialog(self.mainWindow, "Please select a module to load", os.getcwd(), wildcard='python files (*.py)|*.py', style=wx.FD_OPEN)
      if dlg.ShowModal() == wx.ID_CANCEL: return

      filePath = dlg.GetPath()
      try:
         with open(filePath, 'r') as pyFile:
            read_data = pyFile.readlines()
         self.buildGUI(read_data)
      except Exception, e:
         print e

   def buildGUI(self, data=[]):
      progString = ''
      for line in data:
         varRegEx = r'^[A-Za-z]+ = [0-9]+'
         comment = ''
         try:
            line, comment = string.split(line, '#')
         except:
            pass
         varLine = re.match(varRegEx, line)

         if varLine:
            print varLine.group(0), comment
            exec(varLine.group(0))
         else:
            progString += '%s\n' % line

      exec(progString)