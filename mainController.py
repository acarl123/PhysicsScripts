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
      self.progString = ''
      self.vars = {}
      for line in data:
         varRegEx = r'^[A-Za-z]+ = [0-9]+'
         comment = ''
         try:
            line, comment = string.split(line, '#')
         except:
            pass
         varLine = re.match(varRegEx, line)

         if varLine:
            varLine = varLine.group(0)
            varName, initValue = string.split(varLine, '=')
            varName = varName.strip()
            self.vars[varName] = initValue
            self.addControl(wx.TextCtrl, varName, initValue, comment)

         else:
            self.progString += '%s\n' % line

      self.mainWindow.GetSizer().AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
      self.btnRun = wx.Button(self.mainWindow, wx.ID_ANY, u'Run Program', wx.DefaultPosition, wx.DefaultSize, 0)
      self.mainWindow.GetSizer().Add(self.btnRun, 0, wx.ALL, 5)
      self.mainWindow.Layout()
      self.mainWindow.Fit()

      self.mainWindow.Bind(wx.EVT_BUTTON, self.onExec, self.btnRun)

   def addControl(self, type, labelName, initValue, tooltip=None):
      labelName = labelName.strip()
      initValue = initValue.strip()
      # Creates a label diplaying var name
      exec('self.lbl%s = wx.StaticText(self.mainWindow, wx.ID_ANY, u\'%s\', wx.DefaultPosition, wx.DefaultSize, 0)' % (labelName, labelName)) in globals(), locals()
      exec('self.lbl%s.Wrap(-1)' % labelName) in globals(), locals()
      exec('self.mainWindow.GetSizer().Add(self.lbl%s, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5)' % labelName) in globals(), locals()

      # Creates a text box with the default value assigned in the program
      exec('self.txt%s = wx.TextCtrl(self.mainWindow, wx.ID_ANY, u\'%s\', wx.DefaultPosition, wx.DefaultSize, 0)' % (labelName, initValue)) in globals(), locals()
      exec('self.mainWindow.GetSizer().Add(self.txt%s, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)' % labelName) in globals(), locals()
      if tooltip:
         tooltip = tooltip.strip()
         exec('self.txt%s.SetToolTip(wx.ToolTip("%s"))' % (labelName, tooltip)) in globals(), locals()
      # Bind to textbox losing focus for input checking
      self.mainWindow.Bind(wx.EVT_KILL_FOCUS, lambda event: self.onTextChange(event, labelName), eval('self.txt%s' % labelName))

      self.mainWindow.Fit()

   def onTextChange(self, event, ctrlName):
      print 'click', ctrlName

   def onExec(self, event):
      locals().update(self.vars)
      # exec(self.progString)
      eval(compile(self.progString, 'None', 'exec'))