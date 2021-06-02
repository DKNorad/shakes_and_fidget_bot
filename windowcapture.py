import win32gui, win32ui, win32con
import re
import numpy as np
from ctypes import windll
import cv2 as cv


class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, rgx):
        self.rgx = rgx

        # find the handle for the game we want to capture
        self.hwnd = win32gui.FindWindow(None, self.get_game_title())

        # check if window is minimized and maximize it
        w_placement = win32gui.GetWindowPlacement(self.hwnd)
        if w_placement[1] == win32con.SW_SHOWMINIMIZED:
            win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWDEFAULT)

        # get game window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        # border_pixels = 8
        # titlebar_pixels = 30
        # self.w = self.w - (border_pixels * 2)
        # self.h = self.h - titlebar_pixels - border_pixels
        # self.cropped_x = border_pixels
        # self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        # self.offset_x = window_rect[0] + self.cropped_x
        # self.offset_y = window_rect[1] + self.cropped_y

    def get_hwnd(self):
        return self.hwnd

    def get_game_title(self):
        # get full game title with regex
        name_re = re.compile(self.rgx)
        # start by getting a list of all the windows:
        cb = lambda x, y: y.append(x)
        windows = []
        win32gui.EnumWindows(cb, windows)
        # iterate over all found windows and check the titles
        for app in windows:
            txt = win32gui.GetWindowText(app)
            if name_re.match(txt):
                win32gui.GetForegroundWindow()
                return txt
        raise Exception(f"Game not found: {self.rgx}")

    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, 0), win32con.SRCCOPY)

        windll.user32.PrintWindow(self.hwnd, cDC.GetSafeHdc(), 2)

        # save the screenshot
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free Resources
        win32gui.DeleteObject(dataBitMap.GetHandle())
        cDC.DeleteDC()
        dcObj.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)

        cv.imwrite('images/main_screen.jpg', img)
