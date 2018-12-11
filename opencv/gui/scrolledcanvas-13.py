import wx

"""
簪考 https://github.com/wxWidgets/Phoenix/issues/566 ，
在 <user-home>/.pylintrc 裡面加一行
extension-pkg-whitelist = wx, win32api, win32file, win32process
可以讓關於 wx.* 的 intellsense 生效
"""
###
class MyScrolledCanvas(wx.ScrolledCanvas):
    def __init__(self, parent):
        wx.ScrolledCanvas.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonDown, self)
        self.image=None
        self.bitmap=None
        #self.SetVirtualSize((800,600))
        #self.image = wx.Image("d:/mia/Mia201711261136.jpg")
        #self.bitmap = wx.Bitmap(self.image)
        #self.SetVirtualSize((self.image.GetWidth(),self.image.GetHeight()))
        self.SetScrollRate(20, 30)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        if not self.bitmap is None:
            dc.DrawBitmap(self.bitmap, 0, 0)
        #dc.SetPen(wx.Pen('red'))
        #dc.SetBrush(wx.Brush('red'))
        #dc.DrawCircle(20, 20, 10)
        #w, h = self.GetVirtualSize()
        #dc.DrawCircle(w/2, h/2, 10)
        #dc.DrawCircle(w-20, h-20, 10)
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

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.scrolledCanvas= MyScrolledCanvas(self)
        self.controlPanel=ControlPanel(self)
        self.sizer=wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.scrolledCanvas,3, wx.EXPAND)
        self.sizer.Add(self.controlPanel,1, wx.EXPAND)
        self.SetSizer(self.sizer)

class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.btnLoad=wx.Button(self,id=wx.ID_ANY,label="Load")
        self.Bind(wx.EVT_BUTTON,self.onBrowse,self.btnLoad)
        self.photoPath=wx.TextCtrl(self, size=(200,-1))
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.sizerImageFile=wx.BoxSizer(wx.HORIZONTAL)
        self.sizerImageFile.Add(self.photoPath,1,wx.EXPAND)
        self.sizerImageFile.Add(self.btnLoad,0, wx.EXPAND)
        self.sizer2=wx.BoxSizer(wx.HORIZONTAL)
        self.btnRotate90=wx.Button(self,id=wx.ID_ANY,label="Rotate90")
        self.Bind(wx.EVT_BUTTON,self.onRotate90,self.btnRotate90)
        self.sizer2.Add(self.btnRotate90,0,wx.LEFT)
        self.sizer.Add(self.sizerImageFile,0,wx.EXPAND)
        self.sizer.Add(self.sizer2,0,wx.TOP)
        self.SetSizer(self.sizer)

    def onBrowse(self, event):
        """ 
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.ID_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoPath.SetValue(dialog.GetPath())
            self.GetParent().scrolledCanvas.loadImage(file=self.photoPath.GetValue())
        dialog.Destroy() 
    def onRotate90(self, event):
        self.GetParent().scrolledCanvas.image=self.GetParent().scrolledCanvas.image.Rotate90()
        self.GetParent().scrolledCanvas.arrangeImage()
        #self.GetParent().scrolledCanvas.bitmap=wx.Bitmap(self.GetParent().scrolledCanvas.image)
        #self.GetParent().scrolledCanvas.Refresh()
    


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        #self.scrolledCanvas= MyScrolledCanvas(self)
        self.panel=MainPanel(self)

app = wx.App(False)
frm = MyFrame(None, title='Whopper')
frm.Show()
app.MainLoop()
