from time import sleep

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


def createCity(world):

    pyautogui.press('b')
    sleep(0.5)
    newCityNumber = len(world.getPlayerCivilization().getCities()) + 1
    newCityName = f'city{newCityNumber}'

    for char in newCityName:
        pyautogui.press(char)
        sleep(0.1)
    pyautogui.press('enter')
    sleep(2)
    pyautogui.press('space')

    return newCityName

def findCity(cityName):
    pyautogui.hotkey('shift', '?')
    sleep(0.1)
    for char in cityName:
        pyautogui.press(char)
    pyautogui.press('enter')
    sleep(0.1)

def openCityStatus():
    pyautogui.press('f1')
    sleep(0.5)

def openMilitaryTab():
    pyautogui.press('f2')
    sleep(0.5)

def openIntelligenceTab():
    pyautogui.press('f3')
    sleep(0.5)

def openAttitudeTab():
    pyautogui.press('f4')
    sleep(0.5)

def openTradeTab():
    pyautogui.press('f5')
    sleep(0.5)

def openScienceTab():
    pyautogui.press('f6')
    sleep(0.5)

def openWondersTab():
    pyautogui.press('f7')
    sleep(0.5)

def openTop5CitiesTab():
    pyautogui.press('f8')
    sleep(0.5)

def openScoreTab():
    pyautogui.press('f9')
    sleep(0.5)

def openWorldMapTab():
    pyautogui.press('f10')
    sleep(0.5)


