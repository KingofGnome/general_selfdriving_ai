from ctypes import byref, wintypes, windll
import win32gui
import numpy as np
import win32ui
import win32con
import cv2


#If a class has only init and one method, it shouldn't be a class
class Screenshoter:
    def __init__(self, window_name):
        self.hwin = win32gui.GetDesktopWindow()

        hwnd = windll.user32.FindWindowW(None, window_name)
        print("hwnd: ", hwnd)

        r = wintypes.RECT()
        windll.user32.GetWindowRect(hwnd, byref(r))
        self.width = r.right - r.left
        self.height = r.bottom - r.top
        self.left, self.top = r.left, r.top

    def grab_screenshot(self):
        hwindc = win32gui.GetWindowDC(self.hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, self.width, self.height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (self.width, self.height), srcdc, (self.left, self.top), win32con.SRCCOPY)

        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.height, self.width, 4)

        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(self.hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)