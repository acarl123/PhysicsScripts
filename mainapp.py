import wx
from mainController import mainController

def __main():
   app = wx.App(None)
   frame = mainController()
   frame.show()
   app.MainLoop()


if __name__ == '__main__':
    __main()