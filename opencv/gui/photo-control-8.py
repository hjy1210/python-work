import os
import wx
import wx.lib.scrolledpanel as scrolled

# copy from http://www.blog.pythonlibrary.org/2010/03/26/creating-a-simple-photo-viewer-with-wxpython/ 
class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')
 
        self.panel = wx.Panel(self.frame)
        self.PhotoMaxSize = 240
 
        self.createWidgets()
        self.frame.Show()
 
    def createWidgets(self):
        instructions = 'Browse for an image'
        img = wx.Image(240,240)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img))
        self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self.on_clic)
        instructLbl = wx.StaticText(self.panel, label=instructions)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200,-1))
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
        drawBtn = wx.Button(self.panel, label='Draw')
        drawBtn.Bind(wx.EVT_BUTTON, self.drawSomething)
 
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn, 0, wx.ALL, 5)        
        self.sizer.Add(drawBtn, 0, wx.ALL, 5)        
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
 
    def onBrowse(self, event):
        """ 
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.ID_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy() 
        self.onView()
 
    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        #img = img.Scale(NewW,NewH)
        img = img.Scale(W,H)
        self.bitmap = wx.Bitmap(img)
        self.imageCtrl.SetBitmap(self.bitmap)
        self.panel.Refresh()
    def drawSomething(self, event):
        # https://stackoverflow.com/questions/11189471/how-to-draw-a-rectangle-on-a-wx-staticbitmap-image-in-wxpython
        dc= wx.MemoryDC(self.bitmap)
        dc.DrawRectangle(10,10,100,100)
        self.imageCtrl.SetBitmap(self.bitmap)
        self.panel.Refresh()
        dc.SelectObject(wx.NullBitmap) #This de-selects the bitmap
    def on_clic(self, event):
        print(event,event.x,event.y,event.altDown, event.controlDown, event.shiftDown)
        #print(dir(event))
        dc= wx.MemoryDC(self.bitmap)
        dc.DrawRectangle(10,10,20,30)
        self.imageCtrl.SetBitmap(self.bitmap)
        self.panel.Refresh()
        dc.SelectObject(wx.NullBitmap) #This de-selects the bitmap

if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()
