from time import sleep

import win32gui
import win32ui
from ctypes import windll
from PIL import Image

from civCapture import getPlayerName


class Buffor():

    def __init__(self):
        self.bufforSS = ['buffor_1.png', 'buffor_0.png']

    def addToBuffor(self, addBuffor):
        self.bufforSS.append(addBuffor)

    def removeFromBuffor(self, index):
        del self.bufforSS[index]

    def getBuffor(self):
        return self.bufforSS

    def createSSBuffor(self, civWindowTitle):
        variable = 0
        fileName = ''
        for i in range(2):
            hwnd = win32gui.FindWindow(None, civWindowTitle.title)

            # Uncomment the following line if you use a high DPI display or >100% scaling size
            # windll.user32.SetProcessDPIAware()

            # Change the line below depending on whether you want the whole window
            # or just the client area.
            # left, top, right, bot = win32gui.GetClientRect(hwnd)
            left, top, right, bot = win32gui.GetWindowRect(hwnd)
            w = right - left
            h = bot - top - 29

            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()

            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

            saveDC.SelectObject(saveBitMap)

            # Change the line below depending on whether you want the whole window
            # or just the client area.
            # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
            result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)

            im = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)

            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)

            if result == 1:
                fileName = f'buffor_{variable}.png'
                # PrintWindow Succeeded
                im.save(f'buffor_{variable}.png')
                # bufforSS.addToBuffor(f'buffor_{variable}.png')

            variable += 1
            sleep(0.1)
        variable -= 1
        if fileName != '':
            getPlayerName(f'buffor_{variable}.png')