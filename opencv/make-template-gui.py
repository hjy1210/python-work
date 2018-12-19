import os
import wx
import json

class MyScrolledCanvas(wx.ScrolledCanvas):
    def __init__(self, parent):
        wx.ScrolledCanvas.__init__(self, parent)
        self.cursor = wx.Cursor(wx.CROSS_CURSOR)
        self.SetCursor(self.cursor)
        self.Bind(wx.EVT_MOTION,self.OnMotion,self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonDown, self)
        self.template=[]
        self.image=None
        self.bitmap=None
        self.SetScrollRate(20, 30)

    def OnMotion(self,evt):
        u,v=evt.x,evt.y
        x,y=self.CalcUnscrolledPosition(u,v)
        self.GetParent().statusBar.SetStatusText("x={},y={}".format(x,y),1)


    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        if not self.bitmap is None:
            dc.DrawBitmap(self.bitmap, 0, 0)
            for v in self.template:
                dc.SetBrush(wx.Brush("white",style=wx.BRUSHSTYLE_TRANSPARENT))
                dc.SetPen(wx.Pen("red"))
                dc.DrawRectangle(v["lt"][0],v["lt"][1],v["rb"][0]-v["lt"][0],v["rb"][1]-v["lt"][1])
                if "children" in v.keys():
                    for child in v["children"]:
                        if child["type"]=="rectangle":
                            dc.SetPen(wx.Pen("blue"))
                            dc.DrawRectangle(child["lt"][0],child["lt"][1],child["rb"][0]-child["lt"][0],child["rb"][1]-child["lt"][1])
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

        self.statusBar=self.CreateStatusBar(2) # A StatusBar with two field in the bottom of the window
        self.SetStatusBar(self.statusBar)

        #self.CreateStatusBar() 

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
        menuOpen.SetBitmap(wx.Bitmap("opencv/bitmaps/fileopen.png"))  ##### must SetBitmap before append to menu
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
        self.btnLoadTemplate = wx.Button(self,wx.ID_ANY,"載入模板")
        self.Bind(wx.EVT_BUTTON, self.OnLoadTemplate)
        self.controlSizer.Add(self.photoPath,0,wx.EXPAND)
        self.controlSizer.Add(self.btnLoadTemplate,0,wx.EXPAND)


        # Set mainSizer
        self.mainSizer=wx.BoxSizer(wx.HORIZONTAL)
        self.scrolledCanvas= MyScrolledCanvas(self)
        self.mainSizer.Add(self.scrolledCanvas,3, wx.EXPAND)
        self.mainSizer.Add(self.controlSizer,1,wx.EXPAND)
        self.SetSizerAndFit(self.mainSizer)

        self.Show(True)

    def OnLoadTemplate(self,evt):
        """ 
        Browse for template file
        """
        wildcard = "JSON files (*.json)|*.json"
        dialog = wx.FileDialog(None, "Choose a template file",
                               wildcard=wildcard,
                               style=wx.ID_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            with open(dialog.GetPath(), "r") as read_file:
                self.scrolledCanvas.template=json.load(read_file)
            self.drawTemplate()
        dialog.Destroy() 

    def drawTemplate(self):
        self.scrolledCanvas.Refresh()

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
