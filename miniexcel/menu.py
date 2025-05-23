import wx
from pathlib import Path
#from miniexcel.main import cache_path
from miniexcel.table_display import TableChildFrame



class MainMDIFrame(wx.MDIParentFrame):
    def __init__(self, cache_path: str, work_dir: str):
        super().__init__(None, title="CSV Reader", size=(800, 600))
        self.cache_path = Path(cache_path)
        self.work_dir = work_dir
        # Инициализация интерфейса
        self.init_ui()

        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Создаем меню
        menubar = wx.MenuBar()

        # Меню "File"
        file_menu = wx.Menu()
        
        # Пункты меню "File"
        open_item = file_menu.Append(wx.ID_OPEN, "Open\tCtrl+O", "Open a file")
        save_item = file_menu.Append(wx.ID_SAVE, "Save\tCtrl+S", "Save the file")
        save_as_item = file_menu.Append(wx.ID_SAVEAS, "Save As", "Save the file with a new name")
        on_close_current_item = file_menu.Append(wx.ID_CLOSE, "Close table\tCtrl+W", "Close current table")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "Exit\tCtrl+Q", "Exit the application")


        # Меню "Help" (кнопка About)
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, "About", "About this application")
        
        # Добавляем меню в менюбар
        menubar.Append(file_menu, "&File")
        menubar.Append(help_menu, "&Help")
    
        # Устанавливаем менюбар в окно
        self.SetMenuBar(menubar)
    

        # Привязка событий
        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_MENU, self.on_save_as, save_as_item)
        self.Bind(wx.EVT_MENU, self.on_close_current, on_close_current_item)

        # Показываем окно
        self.Show()



    def on_open(self, event):
        """Обработчик для Open"""
        with wx.FileDialog(self, "Open file", wildcard="Text files (*.csv)|*.csv",
                          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:

            file_dialog.SetDirectory(self.work_dir)
            
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            
            path = file_dialog.GetPath()
            frame = TableChildFrame(self, path)
            frame.Show()



    def on_save(self, event):
        """Обработчик для Save"""
        active_child = self.GetActiveChild()
        #print(active_child.get_current_data())
        active_child.table.save()

        
    def on_save_as(self, event):
        """Обработчик для Save"""
        active_child = self.GetActiveChild()
        with wx.FileDialog(self, "Save file", wildcard="Text files (*.csv)|*.csv",
                          style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:

            file_dialog.SetDirectory(self.work_dir)
            
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            
            path = file_dialog.GetPath()
            #print(active_child.get_current_data())
            active_child.table.save_as(path)       


    def on_close_current(self, event):
        """Закрытие активной таблицы"""
        active_child = self.GetActiveChild()
        #print(active_child.get_current_data())
        if active_child:
            active_child.Close()
    

    def on_exit(self, event):
        """Обработчик для Exit"""
        self.Close()