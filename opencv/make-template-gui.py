import os
import wx

class MyScrolledCanvas(wx.ScrolledCanvas):
    def __init__(self, parent):
        wx.ScrolledCanvas.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonDown, self)
        self.image=None
        self.bitmap=None
        self.SetScrollRate(20, 30)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        if not self.bitmap is None:
            dc.DrawBitmap(self.bitmap, 0, 0)
    def loadImage(self,file):
        self.image = wx.Image(file, wx.BITMAP_TYPE_ANY)
        self.arrangeImage()
    def arrangeImage(self):
        self.bitmap = wx.Bitmap(self.image)
        self.SetVirtualSize((self.image.GetWidth(),self.image.GetHeight()))
        self.Refresh()


    def OnLeftButtonDown(self, evt):
        print("Position={},x={},y={},altDown={},shiftDown={},controlDown={},GetScrollPixelsPerUnit()={},CalcScrolledPosition(,)={},CalcUnScrolledPosition(,)={}".format(
            evt.Position, evt.x, evt.y, evt.altDown, evt.shiftDown, evt.controlDown, 
            self.GetScrollPixelsPerUnit(),
            self.CalcScrolledPosition(evt.x, evt.y),
            self.CalcUnscrolledPosition(evt.x, evt.y)))

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))


        self.CreateStatusBar() # A StatusBar in the bottom of the window

        toolbar = self.CreateToolBar()
        oTool = toolbar.AddTool(wx.ID_ANY, '&Open', wx.Bitmap('opencv/bitmaps/fileopen.png'), "Open an existing image file")
        toolbar.Realize()
        self.SetToolBar(toolbar)


        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        
        # menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open file")
        menuOpen = wx.MenuItem(filemenu,wx.ID_OPEN,"&Open"," Open an existing image file")
        menuOpen.SetBitmap(wx.Bitmap("opencv/bitmaps/fileopen.png"))
        filemenu.Append(menuOpen)

        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Bind(wx.EVT_TOOL, self.OnOpen, oTool)

        # Set controlSizer
        self.controlSizer=wx.BoxSizer(wx.VERTICAL)
        self.photoPath = wx.TextCtrl(self)
        self.photoPath.SetEditable(False)
        self.controlSizer.Add(self.photoPath,0,wx.EXPAND)


        # Set mainSizer
        self.mainSizer=wx.BoxSizer(wx.HORIZONTAL)
        self.scrolledCanvas= MyScrolledCanvas(self)
        self.mainSizer.Add(self.scrolledCanvas,3, wx.EXPAND)
        self.mainSizer.Add(self.controlSizer,1,wx.EXPAND)
        self.SetSizerAndFit(self.mainSizer)

        self.Show(True)

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "A small template editor", "About Make-Template", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.
    def OnOpen(self, event):
        """ 
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg|(*.png)|*.png"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.ID_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoPath.SetValue(dialog.GetPath())
            self.scrolledCanvas.loadImage(file=self.photoPath.GetValue())
        dialog.Destroy() 

app = wx.App(False)
frame = MainWindow(None, "Template Maker")
app.MainLoop()
