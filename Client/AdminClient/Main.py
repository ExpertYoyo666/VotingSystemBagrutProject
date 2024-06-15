import wx
from Model import Model
from MainFrame import MainFrame
from Controller import Controller
from Protocol import Protocol

if __name__ == '__main__':
    app = wx.App()
    model = Model()
    main_frame = MainFrame("Digital Voting System Admin Client")
    main_frame.Show()
    protocol = Protocol()
    c = Controller(model, main_frame, protocol)

    app.MainLoop()
