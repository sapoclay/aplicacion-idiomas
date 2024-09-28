import wx
import threading
import sys

class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, icon):
        super().__init__()
        self.SetIcon(icon, "Aplicación de Idiomas")
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_left_double_click)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.on_right_click)
        self.Bind(wx.adv.EVT_TASKBAR_MENU, self.on_right_click)

        # Create a menu
        self.menu = wx.Menu()
        open_item = self.menu.Append(wx.ID_ANY, "Abrir App")
        self.menu.AppendSeparator()
        close_item = self.menu.Append(wx.ID_ANY, "Cerrar App")
        
        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_exit, close_item)

    def CreatePopupMenu(self):
        return self.menu

    def on_left_double_click(self, event):
        self.on_open(event)

    def on_right_click(self, event):
        self.PopupMenu(self.menu)

    def on_open(self, event):
        # Aquí puedes agregar el código para abrir la aplicación
        print("Abriendo la aplicación...")
        wx.CallAfter(wx.GetApp().Show)

    def on_exit(self, event):
        wx.CallAfter(wx.GetApp().Exit)

def start_tray_icon(icon_path):
    app = wx.App(False)  # Create a new wx.App
    icon = wx.Icon(icon_path)  # Load your icon
    TrayIcon(icon)  # Create the tray icon
    app.MainLoop()  # Start the wxPython event loop

def run_tray_icon(icon_path):
    thread = threading.Thread(target=start_tray_icon, args=(icon_path,))
    thread.start()
