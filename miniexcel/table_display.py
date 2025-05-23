import wx
import wx.grid
import wx.lib.mixins.inspection

import string

from miniexcel.load_manager import LoadManager

class TableChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, filename: str):
        super().__init__(parent, title=filename.split('/')[-1], size=(500, 300))

        # таблица
        self.table = EditableGridTable(filename)
        self.grid = wx.grid.Grid(self)
        self.grid.SetTable(self.table, takeOwnership=True)
        self.grid.EnableEditing(True)
        
        # кнопка масштабирования
        self.btn_autosize = wx.Button(self, label="AutoSize")
        self.btn_autosize.Bind(wx.EVT_BUTTON, self.on_autosize)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.btn_autosize, flag = wx.ALIGN_CENTER | wx.ALL, border = 10)
        sizer.Add(self.grid, flag = wx.ALIGN_CENTER)
        #sizer.Add(self.grid, 1, wx.ALL, 10)
        #sizer.Add(self.grid, 1, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        self.Layout()
        
        self.Bind(wx.EVT_CLOSE, self.on_close)


    def on_autosize(self, event):
        """Масштабирует таблицу  под размер содержимого CSV-файла"""
        self.grid.AutoSizeColumns()
        self.grid.AutoSizeRows()
        self.Layout()



    
    def on_close(self, event):
        """Обработчик закрытия таблицы"""
        # Реально уничтожаем окно
        self.Destroy()

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