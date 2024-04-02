import pygetwindow
import pyautogui
import win32api
import win32con
import win32gui
from pywinauto.findwindows    import find_window

from ctypes import windll
import win32ui
import matplotlib.pyplot as plt
from PIL import Image


def findAllWindows():
    for x in pyautogui.getAllWindows():
        if 'Program:' in x.title and 'CIV' in x.title:
            return (x)

def takeSreenShoot(civWindowTitle):
    hwnd = win32gui.FindWindow(None, civWindowTitle.title)

    # Uncomment the following line if you use a high DPI display or >100% scaling size
    # windll.user32.SetProcessDPIAware()

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top - 50

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
        # PrintWindow Succeeded
        im.save("test.png")

def analyzeSS():

    im = plt.imread('test.png')

    # im = im[0:250 , 50:500, :]
    imgplot = plt.imshow(im)
    plt.show()



def click(civWindow):

    hwnd = win32gui.FindWindowEx(0, 0, 0, civWindow.title)
    win32gui.SetForegroundWindow(hwnd)
    pyautogui.moveTo(civWindow.topleft.x + 250, civWindow.topleft.y + 150, duration = 0)
    pyautogui.click(civWindow.topleft.x + 50, civWindow.topleft.y + 50)

# click(findAllWindows())
# takeSreenShoot(findAllWindows())
analyzeSS()