import wx

"""
簪考 https://github.com/wxWidgets/Phoenix/issues/566 ，
在 <user-home>/.pylintrc 裡面加一行
extension-pkg-whitelist = wx, win32api, win32file, win32process
可以讓關於 wx.* 的 intellsense 生效
"""
###
class MyScrolledWindow(wx.ScrolledWindow):
    def __init__(self, *args, **kw):
        wx.ScrolledWindow.__init__(self, *args, **kw)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonDown, self)
        self.SetVirtualSize((63000, 3000))
        self.SetScrollRate(20, 30)
        self.image = wx.Image("d:/mia/Mia201711261136.jpg")
        self.bitmap = wx.Bitmap(self.image)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)

        dc.SetPen(wx.Pen('red'))
        dc.SetBrush(wx.Brush('red'))
        dc.DrawBitmap(self.bitmap, 0, 0)
        dc.DrawCircle(20, 20, 10)
        w, h = self.GetVirtualSize()
        dc.DrawCircle(w/2, h/2, 10)
        dc.DrawCircle(w-20, h-20, 10)

    def OnLeftButtonDown(self, evt):
        print("Position={},x={},y={},altDown={},shiftDown={},controlDown={},GetScrollPixelsPerUnit()={},CalcScrolledPosition(,)={},CalcUnScrolledPosition(,)={}".format(
            evt.Position, evt.x, evt.y, evt.altDown, evt.shiftDown, evt.controlDown, 
            self.GetScrollPixelsPerUnit(),
            self.CalcScrolledPosition(evt.x, evt.y),
            self.CalcUnscrolledPosition(evt.x, evt.y)))


app = wx.App(False)
frm = wx.Frame(None, title='Whopper')
sw = MyScrolledWindow(frm)
frm.Show()
app.MainLoop()
