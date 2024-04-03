import glob
from time import sleep

import cv2
import numpy
import numpy as np
import pygetwindow
import pyautogui
import win32api
import win32con
import win32gui

from ctypes import windll
import win32ui
import matplotlib.pyplot as plt
from PIL import Image

import mapTiles
import mapWorld
from mapTile import MapTile

world = mapWorld.MapWorld()
colorVariant = cv2.COLOR_RGB2BGR

def findAllWindows():
    for x in pyautogui.getAllWindows():
        if 'Program:' in x.title and 'CIV' in x.title:
            return (x)

def takeSreenShoot(civWindowTitle):
    variable = 0

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
            # PrintWindow Succeeded
            im.save(f'test_{variable}.png')
        variable += 1
        sleep(0.05)

def checkIfImageHasObj(image, template):

    print(image.shape)
    image = cv2.cvtColor(image, colorVariant)
    template = cv2.cvtColor(template, colorVariant)

    heat_map = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # plt.imshow(image)
    # plt.figure()
    # plt.imshow(template)
    # plt.show()
    # print(heat_map)
    print(np.amax(heat_map))

    threshold = 0.85
    if np.amax(heat_map) > threshold:
        h, w, _ = template.shape
        y, x = np.unravel_index(np.argmax(heat_map), heat_map.shape)

        print(x, y)

        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)
        #
        # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        #
        # plt.show()

        return x, y
    else:
        return -1, -1

def findShapes(mode, checkingTileOrUnit = None):

    if mode == 0:
        image = plt.imread('test_1.png')
        template = plt.imread('units/settler.png')

        return checkIfImageHasObj(image, template)

    if mode == 1:
        image = checkingTileOrUnit

        files = glob.glob("tiles/*.png")

        counter = 0
        # loop over list
        for f in files:
            template = plt.imread(f)

            # image[image[:, :, 0] <= 0.35, 0] = 0.40
            # image[image[:, :, 1] <= 0.35, 1] = 0.7
            # image[image[:, :, 2] <= 0.35, 2] = 0.18
            print(image.shape)
            rowIndex = 0
            for row in image:
                columnIndex = 0
                for column in row:
                    if numpy.array([0, 0, 0]) in column and (columnIndex < 10 or 20 < columnIndex < 30) and (rowIndex < 10 or 20 < rowIndex < 30):
                        counter += 1
                    columnIndex +=1
                rowIndex +=1
            print(counter)
            foundX, foundY = checkIfImageHasObj(image, template)

            plt.imshow(image)
            plt.figure()
            plt.imshow(template)
            plt.show()

            if foundX >= 0 and foundY >= 0:
                print(f)
                return foundX, foundY, f.replace('tiles\\', '')
            else:
                print('Nieznany Tile')

def analyzeStartingPosition(x, y):

    if x >= 0 and y >= 0:

        # for i, j in zip(range(-1, 2), range(-1, 2)):
            tileSizeX = 32
            tileSizeY = 32
            tileOffsetX = tileSizeX * 0
            tileOffsetY = tileSizeY * -1
            im = plt.imread('test_0.png')
            plt.axis('off')
            startingPoint = im[y+tileOffsetY:y+tileSizeY+tileOffsetY, x+tileOffsetX:x+tileSizeX++tileOffsetX, :]
            knownTileX, knownTileY, file = findShapes(1, startingPoint)

            if knownTileX == 0 and knownTileY == 0:
                tileEnum = findRightMapTileEnum(file)
                if tileEnum != -1:
                    mapTile = MapTile(0, 0, tileEnum)
                    world.appendMapTile(mapTile)
                    print(world)
                else:
                    print('Enum error')

        # cv2.rectangle(im, (x, y), (x + tileSizeX, y + tileSizeY), (0, 0, 255), 5)
        # imgplot = plt.imshow(startingPoint)
        # plt.show()

def findRightMapTileEnum(tileUrl):

    for e in mapTiles.MapTilesEnums:
        if e.value[1] == tileUrl:
            return e
        else:
            return -1

def click(civWindow):

    hwnd = win32gui.FindWindowEx(0, 0, 0, civWindow.title)
    win32gui.SetForegroundWindow(hwnd)
    pyautogui.moveTo(civWindow.topleft.x + 250, civWindow.topleft.y + 150, duration = 0)
    pyautogui.click(civWindow.topleft.x + 50, civWindow.topleft.y + 50)

# click(findAllWindows())
# takeSreenShoot(findAllWindows())
x,y = findShapes(0)
analyzeStartingPosition(x, y)
