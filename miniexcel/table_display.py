import wx
import wx.grid
import wx.lib.mixins.inspection

import string

from miniexcel.load_manager import LoadManager

class TableChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, filename: str):
        super().__init__(parent, title=filename.split('/')[-1], size=(500, 300))
        
        self.table = EditableGridTable(filename)
        
        self.grid = wx.grid.Grid(self)
        self.grid.SetTable(self.table, takeOwnership=True)
        self.grid.EnableEditing(True)
        self.grid.AutoSizeColumns()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
    
    def on_close(self, event):
        """Перехватываем закрытие, чтобы не удалять фрейм полностью"""
        self.Iconize()  # Сворачиваем вместо закрытия
        # self.Destroy()  # Раскомментировать для реального закрытия

class EditableGridTable(wx.grid.PyGridTableBase):
    def __init__(self, filename):
        super().__init__()
        load_manader = LoadManager('.')
        self.data = load_manader.load(filename)
        self.col_labels = string.ascii_uppercase[:len(self.data[0])]

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.col_labels)

    def GetValue(self, row, col):
        return self.data[row][col]

    def SetValue(self, row, col, value):
        self.data[row][col] = value

    def GetColLabelValue(self, col):
        return self.col_labels[col]

    def IsEmptyCell(self, row, col):
        return False