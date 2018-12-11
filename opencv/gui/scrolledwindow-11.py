#!/usr/bin/python

import wx

class FicheFrame( wx.Frame ) :

    def __init__( self ) :

        wx.Frame.__init__( self, None,-1, "FicheFrame", size=(300, 400) )
        #scrollWin = wx.ScrolledCanvas( self, -1 )
        scrollWin = wx.ScrolledWindow( self, -1 )
        
        x = 20       # Magic numbers !?
        y = 20
        for i in range( 50 ) :

            txtStr = " Text %02d  : " % (i+1)
            stTxt = wx.StaticText( scrollWin, -1, txtStr, pos=(x, y) )

            w, h = stTxt.GetSize()
            txtCtrl = wx.TextCtrl( scrollWin, -1, pos=(x+w+5, y) )

            dy = h + 10     # calculate for next loop
            y += dy

        #end for
        """
        img=wx.Image(400,300)
        imageCtrl = wx.StaticBitmap(scrollWin, wx.ID_ANY, wx.Bitmap(img))
        img2 = wx.Image("d:/mia/Mia201711261136.jpg")
        imageCtrl.SetBitmap(wx.Bitmap(img2))
        """
        scrollWin.SetScrollbars( 0, dy,  0, y/dy+1 )
        #scrollWin.SetScrollbars( 0, 10,  0,10 )
        scrollWin.SetScrollRate( 1, 1 )      # Pixels per scroll increment

    #end __init__ def

#end class

if __name__ == '__main__' :

    myapp = wx.App( redirect=False )

    myAppFrame = FicheFrame()
    myAppFrame.Show()

    myapp.MainLoop()
