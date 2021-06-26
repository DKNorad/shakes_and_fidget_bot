from ctypes import windll
import cv2 as cv
import numpy as np
import re
import win32gui, win32ui, win32con, win32process


class WindowCapture:
    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    game_title = None

    def __init__(self, rgx=r".*Shakes & Fidget \(.*\)"):
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

    def get_pid(self):
        _, pid = win32process.GetWindowThreadProcessId(self.hwnd)
        return pid

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
        win_dc = win32gui.GetWindowDC(self.hwnd)
        dc_obj = win32ui.CreateDCFromHandle(win_dc)
        create_dc = dc_obj.CreateCompatibleDC()
        data_bitmap = win32ui.CreateBitmap()
        data_bitmap.CreateCompatibleBitmap(dc_obj, self.w, self.h)
        create_dc.SelectObject(data_bitmap)
        create_dc.BitBlt((0, 0), (self.w, self.h), dc_obj, (0, 0), win32con.SRCCOPY)

        windll.user32.PrintWindow(self.hwnd, create_dc.GetSafeHdc(), 2)

        # save the screenshot
        signed_array = data_bitmap.GetBitmapBits(True)
        img = np.frombuffer(signed_array, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        cv.imwrite('images/main_screen.jpg', img)

        # free Resources
        win32gui.DeleteObject(data_bitmap.GetHandle())
        create_dc.DeleteDC()
        dc_obj.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, win_dc)

