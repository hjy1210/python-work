# matplotlib.pyplot

## keypress-demo.py
示範 matplotlib 鍵盤事件
* 'q' -> 離開
* 'f' -> 切換全螢幕
* 'x' -> 切換 xlabel 是否顯現
* `<other-key>` -> 印出 key

## pick_event_demo.py
用四個 matplotlib 圖形示範各種選取事件

## rotate.py
示範用opencv做圖形旋轉

## template-match.py
用 ch10-15.png 為模板(template)，定位其在 9-302-203-29-1-1-1.jpg 檔案的位置，
採取的定位方法有 'cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED'等六種方法，
結果是：除了 'cv.TM_CCORR' 外都成功。

註：用 matplotlib 顯示圖形。

## ch-template-match.py
選定一個資料夾，採用 cv.TM_CCOEFF_NORMED 方法，以 ch10-15.png 為模板，對目錄夾裡面每一個 .png/.jog 檔案進行定位，列出定位位置與信度，必要時顯示圖形，同時將定位出來的部分合併成opencv/data/output.jpg

# cv.imshow
## make-template-0.py
製作模板所需的ROI
* 用滑鼠拖拉出 ROI
* 'r' 放棄 ROI
* 'c' 擷取 ROI，顯示在另一視窗 -> <any-key> -> 離開

## make-template.py
製作模板所需的ROI
* ctrl+leftbuttondown -> cropping -> 拖拉出 ROI，連續做可以得到 ROI 列
* leftbuttondown -> moving -> 滑鼠移動產生移動圖形的功能
* 'c' -> 展示結果 -> `<any-key>` -> 離開，同時產生template-*.jpg

## 雜項
參考 [Pylint not detecting any wx objects/members #566](https://github.com/wxWidgets/Phoenix/issues/566)，
在 `<user-home>/.pylintrc` 裡面加一行
```
extension-pkg-whitelist = wx, win32api, win32file, win32process
```
可以讓關於 wx.* 的 VSCode intellsense 生效

# GUI - WxPythom
[wxPython API Documentation](https://wxpython.org/Phoenix/docs/html/index.html) 可以找到詳細說明。
## wxpywiki 
[Getting Started](https://wiki.wxpython.org/Getting%20Started)
* helloworld-1.py wx.App, wx.Frame, window.Show, app.MainLoop
* texteditor-2.py wx.TextCtrl
* menubar-3.py wx.Menu, wx.MenuBar, wx.StatusBar
* event-handling-4.py window.Bind, wx.MessageDialog, dialog.ShowModal, window.Destroy, window.Close,
wx.FileDialog, 
* sizer-5.py wx.BoxSizer, wx.Button, windows.SetSizer, window.SetSizerAndFit
* control-6.py wx.StaticText, wx.TextCtrl, wx.Button, wx.ComboBox, wx.CheckBox, wx.RadioBox
* draw-line-7.py wx.PaintDC, dc.DrawLine, wx.PaintEvent
* photo-control-8.py wx.Image, wx.StaticBitmap, window.Refresh, image.Scale, wx.MemoryDC, dc.SelectObject(wx.NullBitmap)
        Publisher.subscribe(self.updateImages, "updateimages")
* image_viewer2-10.py `pip install pypubsub`, `from pubsub import pub as Publisher` 成功。wx.Timer, 
pub.subscribe, pub.sendMessage
* scrolledcanvas-13.py wx.ScrolledCanvas, scrolled.SetScrollRate, dc.DrawBitmap, 
window.SetVirtualSize, scrolled.CalcUnscrolledPosition, scrolled.CalcScrolledPosition, wx.MouseEvent

## [wxPython tutorial](http://zetcode.com/wxpython/)
wx.PaintDC, dc.DrawLine, wx.Colour, wx.Pen, dc.SetPen, wx.Brush, dc.SetBrush, dc.DrawRectangle,
wx.JOIN_MITER, wx.CAP_ROUND, pen.SetJoin, pen.SetCap, dc.GradientFillLinear, wx.SOLID, wx.CROSS_HATCH, dc.DrawPoint, dc.DrawEllipse, dc.DrawArc, dc.SetDeviceOrigion, wx.Region, 
dc.SetDeviceClippingRegion, dc.DestroyClippingRegion, region.Intersect,
window.ClientToScreen, window.GetPosition, window.SetCursor, wx.Cursor, wx.StockCursor,
window.Move
* lines.py Math
* ruler.py ClientToScreen, Move, Cursor
* star.py clipping

# WxPython
要了解 wxPython， 源頭在 [Welcome to the wxPyWiki](https://wiki.wxpython.org/FrontPage)，
* 先看其中的 [Getting started with wxPython](https://wiki.wxpython.org/Getting%20Started)
* 再看 [wxPython tutorial](http://zetcode.com/wxpython/)
* [Index of /wxPython4/extras/4.0.3](https://extras.wxpython.org/wxPython4/extras/4.0.3/) 裡面有wxPython-demo-4.0.3.tar.gz，解壓縮後在demo子目錄裡面執行 `python main.py` 可以看到 wxPython 的各種示範

# [dlib](http://dlib.net/)
dlib 是一個 C++ 函數庫，它有許多機器學習功能，威力強大，可以用 Python 呼叫。

它的功能包括人臉辨識、臉部特徵定位、Support Vector Machine,,,,等等。

##  dlib 的安裝
這個[網頁](http://dlib.net/compile.html)上說
  ```
  Note that you need to have CMake and a working C++ compiler installed for this to work.
  ```
所以
* 安裝 Visual Studio 2017 community edition，選取 C++, Python 功能
* 用 [cmake-3.13.1-win64-x64.msi](https://cmake.org/download/) 安裝 Cmake，並設定路徑包括 CMake\bin 
* 在 Visual Studio 2017 中的 Python 環境用 pip install dlib 來安裝 dlib

## dlib 的 image 格式
dlib 的 image 格式與 opencv 相同，讀取中文路徑的圖檔也與opencv一樣會有問題，可透過 Pillow 來讀取，再轉換成 opencv/dlib格式。
```
from PIL import Image
# 用 Pillow 讀檔
img = Image.open(fn)
# 轉成 opencv 格式
img = np.array(img_clip)
# 轉成 Pil 格式
img = Image.fromarray(img)

```
# opencv 與 dlib 在人臉辨識上的比較
[Face Detection – OpenCV, Dlib and Deep Learning ( C++ / Python )](https://www.learnopencv.com/face-detection-opencv-dlib-and-deep-learning-c-python/) 對 OpenCV 與 Dlib 在人臉辨識功能方面做了詳細的比較，考慮速度、準度、左瞧、右看、低頭、抬頭、遠近、部分遮蔽等性質。有一個47秒的[影片](https://www.youtube.com/watch?time_continue=2&v=kKaU6JFRu5g)，充分展示比較的結果。

若要收集正面照片，對左瞧、右看、低頭、抬頭的相片能夠辨識反而是缺點，所以似應採用 openCV/Haar 方法並使用辨識率較佳的 lbpcascade_frontalface_improved.xml 模型。

# Demo
## Step1
用make-template.py 製作模板所需的ROI
* ctrl+leftbuttondown -> cropping -> 拖拉出 ROI，連續做可以得到 ROI 列
* leftbuttondown -> moving -> 滑鼠移動產生移動圖形的功能
* 'c' -> 展示結果 -> `<any-key>` -> 離開，同時產生template-*.jpg
## Step2
ch-template-match.py 選定一個資料夾，採用 cv.TM_CCOEFF_NORMED 方法，以 ch10-15.png/template-*.jpg 為模板，對目錄夾裡面每一個 .png/.jpg 檔案進行定位，列出定位位置與信度，必要時顯示圖形，同時將定位出來的部分合併成opencv/data/output.jpg。
注意：十個圖形中，定位出來的位置高低相差可達10pixels，一個劃記的高度約為11個pixels而已。

## Step3

直接用 Windows 內建的圖檔顯示器瀏覽錱俞提供的國文卷1目錄，可以看出圖檔由兩頁拼成且影像有飄移現象。
圖檔尺寸完全相同，疑似後端軟體的後製。

先用 make-template-gui.py 手動作出 ch-template.json/ch-template-2.json，裡面有定錨矩形以及連帶的作答方塊(rectangle)與選擇列(sequence)。

再用 template-match-score.py 對 ch-template.json/ch-template-2.json 裡面的非選擇題定位，選擇題定位讀卡並列印出讀卡結果。

讀卡時根據secondRun的第二個參數值True/False決定是否顯示影像。

由 ch-template.json/ch-template-2.json 結果的比較，可看出原來的圖形是由兩頁的A4分別掃描再拼出來的。

初步結論：定錨方塊與作答區域要越靠近越好，最低要求是必須在同一個掃描頁面裡。

## Step4
* 題卷卡印刷時，是否位置、濃淡會一直保持一致。
* 學生是否會在非作答區塗鴉、計算、打草稿，這會影響定位。
* 雙色印刷，可以用來過濾選擇題的框框，增加讀卡的準確度。雙色印刷有別於彩色印刷。

