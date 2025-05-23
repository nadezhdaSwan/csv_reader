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
        #self.Iconize()  # Сворачиваем вместо закрытия
        self.Destroy()  # Раскомментировать для реального закрытия

    def get_current_data(self):
        """Возвращает текущие данные из таблицы"""
        return self.table.data


    







class EditableGridTable(wx.grid.GridTableBase):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.load_manader = LoadManager('.')
        self.data = self.load_manader.load(self.filename)
        self.col_labels = string.ascii_uppercase[:len(self.data[0])]

    def save_as(self, new_filename):
        self.load_manader.save(new_filename,self.data)

    def save(self):
        self.load_manader.save(self.filename,self.data)



    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.col_labels)

    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            wx.LogError(f"Incorrect number of columns")
        

    def SetValue(self, row, col, value):
        self.data[row][col] = value

    def GetColLabelValue(self, col):
        return self.col_labels[col]

    def IsEmptyCell(self, row, col):
        return False

    def GetAttr(self, row, col, kind):
        attr = wx.grid.GridCellAttr()
        # Заливаем каждую вторую строку серым цветом
        if row % 2 == 1:
            attr.SetBackgroundColour(wx.LIGHT_GREY)
        return attr