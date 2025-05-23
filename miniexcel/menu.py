import wx

#from miniexcel.main import cache_path
from miniexcel.table_display import TableChildFrame

class MainMDIFrame(wx.MDIParentFrame):
    def __init__(self, cache_path):
        super().__init__(None, title="CSV Reader", size=(800, 600))
        self.cache_path = cache_path
        
        # Инициализация интерфейса
        self.init_ui()
        self.table_frames = []

        # Таблицы открытые при предыдущем запуске
        self.open_prev_table()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Создаем меню
        menubar = wx.MenuBar()

        # Меню "File"
        file_menu = wx.Menu()
        
        # Пункты меню "File"
        file_menu.Append(wx.ID_OPEN, "Open\tCtrl+O", "Open a file")
        file_menu.Append(wx.ID_SAVE, "Save\tCtrl+S", "Save the file")
        file_menu.Append(wx.ID_SAVEAS, "Save As", "Save the file with a new name")
        file_menu.Append(wx.ID_CLOSE, "Close table\tCtrl+W", "Close current table")
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
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        # Показываем окно
        self.Show()

    def open_prev_table(self):
        '''открываем таблицы в предыдущем сеансе'''
        with open(self.cache_path) as file:
            opened_files = file.read().split('\n')
        for file in opened_files:
            if file[-3:] == 'csv':
                frame = TableChildFrame(self, file)
                frame.Show()
                self.table_frames.append(frame)

    

    def on_exit(self, event):
        """Обработчик для Exit"""
        self.Close()