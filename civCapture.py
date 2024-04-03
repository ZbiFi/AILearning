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
colorVariant = cv2.IMREAD_COLOR

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

    # print(image.shape)
    image = cv2.cvtColor(image, colorVariant)
    template = cv2.cvtColor(template, colorVariant)

    heat_map = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # plt.imshow(image)
    # plt.figure()
    # plt.imshow(template)
    # plt.imshow(heat_map)
    # plt.show()
    # print(heat_map)
    print(f'    {np.amax(heat_map)}')

    threshold = 0.40
    if np.amax(heat_map) > threshold:

        # h, w = template.shape
        h, w, _ = template.shape[::-1]

        y, x = np.unravel_index(np.argmax(heat_map), heat_map.shape)

        # print(x, y)

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
        image = cv2.imread('test_1.png')
        template = cv2.imread('units/settler.png')

        return checkIfImageHasObj(image, template)

    if mode == 1:
        image = checkingTileOrUnit
        tileSizeX = 32
        tileSizeY = 32
        tileSizeXRecuder = 10
        tileSizeYRecuder = 10
        files = glob.glob("tiles/*.png")

        counter = 0

        rowIndex = 0
        image = image[0 + tileSizeYRecuder:tileSizeY - tileSizeYRecuder, 0 + tileSizeXRecuder:tileSizeX - tileSizeXRecuder, :]
        # for row in image:
        #     columnIndex = 0
        #     for column in row:
        #         if numpy.array([0, 0, 0]) in column and (columnIndex < 10 or 20 < columnIndex < 30) and (rowIndex < 10 or 20 < rowIndex < 30):
        #             counter += 1
        #             if counter > 20:
        #                 image = image[0 + tileSizeYRecuder:tileSizeY - tileSizeYRecuder, 0 + tileSizeXRecuder:tileSizeX - tileSizeXRecuder, :]
        #                 break
        #         columnIndex += 1
        #     rowIndex += 1
        #     if counter > 20:
        #         break

        # loop over list
        for f in files:
            template = cv2.imread(f)

            # image[(image[:, :, 0] <= 0.35) & (image[:, :, 1] <= 0.35) & (image[:, :, 2] <= 0.35)] = [0.44, 0.57, 0.18]
            # print(image.shape)

            # print(counter)
            foundX, foundY = checkIfImageHasObj(image, template)

            # plt.imshow(image)
            # plt.figure()
            # plt.imshow(template)
            # plt.show()

            if foundX >= 0 and foundY >= 0:
                # plt.imshow(image)
                # plt.figure()
                # plt.imshow(template)
                # plt.show()
                print(f'--->Found {f}')
                return foundX, foundY, f.replace('tiles\\', '')
            else:

                print(f'    {f} - Nieznany Tile ')

def analyzeStartingPosition(x, y):


    if x >= 0 and y >= 0:

        for i in range(-1, 2):
            for j in range(-1, 2):
                print(f'i: {i} j:{j}')
                tileSizeX = 32
                tileSizeY = 32
                tileOffsetX = tileSizeX * j
                tileOffsetY = tileSizeY * i
                im = cv2.imread('test_0.png')
                plt.axis('off')
                # print(im)
                startingPoint = im[y+tileOffsetY:y+tileSizeY+tileOffsetY, x+tileOffsetX:x+tileSizeX++tileOffsetX, :]

                # imgplot = plt.imshow(startingPoint)
                # plt.show()
                knownTileX, knownTileY, file = findShapes(1, startingPoint)

                # imgplot = plt.imshow(startingPoint)
                # plt.show()
                if knownTileX >= 0 and knownTileY >= 0:
                    tileEnum = findRightMapTileEnum(file)
                    if tileEnum != -1:
                        mapTile = MapTile(j, i, tileEnum)
                        world.appendMapTile(mapTile)
                    else:
                        print('Enum error')

        # cv2.rectangle(im, (x, y), (x + tileSizeX, y + tileSizeY), (0, 0, 255), 5)

    print(world)

def findRightMapTileEnum(tileUrl):

    for e in mapTiles.MapTilesEnums:
        if e.value[1] == tileUrl:
            return e

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
