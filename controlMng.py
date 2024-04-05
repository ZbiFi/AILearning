import pyautogui
import win32gui


def findAllWindows():
    for x in pyautogui.getAllWindows():
        if 'Program:' in x.title and 'CIV' in x.title:
            return (x)

def click(civWindow):

    hwnd = win32gui.FindWindowEx(0, 0, 0, civWindow.title)
    win32gui.SetForegroundWindow(hwnd)
    pyautogui.moveTo(civWindow.topleft.x + 250, civWindow.topleft.y + 150, duration = 0)
    pyautogui.click(civWindow.topleft.x + 50, civWindow.topleft.y + 50)