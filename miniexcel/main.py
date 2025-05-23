import wx
import wx.lib.mixins.inspection

from miniexcel.menu import MainMDIFrame

# settings
work_dir = 'data'
doc_dir = 'doc'
cache_path = '.cache'




if __name__ == "__main__":
    app = wx.lib.mixins.inspection.InspectableApp()
    frame = MainMDIFrame(cache_path, work_dir)
    frame.Show()
    app.MainLoop()


