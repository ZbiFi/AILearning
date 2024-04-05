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
import pytesseract
from ctypes import windll
import win32ui
import matplotlib.pyplot as plt
from PIL import Image

import cities
import mapTiles
import mapWorld
from controlMng import click, findAllWindows
from mapTile import MapTile
from player import Player

world = mapWorld.MapWorld()
colorVariant = cv2.IMREAD_COLOR


def createSSBuffor(civWindowTitle):
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

        variable += 1
        sleep(0.1)
    variable-= 1
    if fileName != '':
        getPlayerName(f'buffor_{variable}.png')

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

    # threshold = 0.5
    # if np.amax(heat_map) > threshold:
    #
    #     # h, w = template.shape
    #     h, w, _ = template.shape[::-1]
    #
    #     y, x = np.unravel_index(np.argmax(heat_map), heat_map.shape)
    #
    #     # print(x, y)
    #
    #     # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)
    #     #
    #     # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    #     #
    #     # plt.show()
    #
    #     return heat_map
    # else:
    return heat_map

def findShapes(mode, checkingTileOrUnit = None):

    if mode == 0:
        image = cv2.imread('buffor_0.png')
        template = cv2.imread('units/settler.png')

        heat_map = checkIfImageHasObj(image, template)
        foundY, foundX = np.unravel_index(np.argmax(heat_map), heat_map.shape)
        return foundX, foundY

    if mode == 1:
        tilesSimilarity = []
        image = checkingTileOrUnit
        tileSizeX = 32
        tileSizeY = 32
        tileSizeXRecuder = 6
        tileSizeYRecuder = 6
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
            heat_map = checkIfImageHasObj(image, template)
            foundY, foundX = np.unravel_index(np.argmax(heat_map), heat_map.shape)
            print(f'    {np.amax(heat_map):.3f} {f}')
            # plt.imshow(image)
            # plt.figure()
            # plt.imshow(template)
            # plt.show()
            tilesSimilarity.append([np.amax(heat_map), f, foundX, foundY])

        tilesSimilarity = sorted(tilesSimilarity, key=lambda x: x[0])

        if tilesSimilarity[len(tilesSimilarity)-1][2] >= 0 and tilesSimilarity[len(tilesSimilarity)-1][3] >= 0:
            # plt.imshow(image)
            # plt.figure()
            # plt.imshow(template)
            # plt.show()
            print(f'--->Found {tilesSimilarity[len(tilesSimilarity)-1][1]}')
            return tilesSimilarity[len(tilesSimilarity)-1][2], tilesSimilarity[len(tilesSimilarity)-1][3], tilesSimilarity[len(tilesSimilarity)-1][1].replace('tiles\\', '')
        else:

            print(f'    {f} - Nieznany Tile ')

        tilesSimilarity = sorted(tilesSimilarity, key=lambda x: x[0])
        print(tilesSimilarity[len(tilesSimilarity)-1])

def analyzeStartingPosition(x, y):

    fileRepo = []
    if x >= 0 and y >= 0:

        for i in range(-1, 2):
            for j in range(-1, 2):
                print(f'i: {i} j:{j}')
                tileSizeX = 32
                tileSizeY = 32
                tileOffsetX = tileSizeX * j
                tileOffsetY = tileSizeY * i
                im = cv2.imread('buffor_1.png')
                plt.axis('off')
                # print(im)
                startingPoint = im[y+tileOffsetY:y+tileSizeY+tileOffsetY, x+tileOffsetX:x+tileSizeX++tileOffsetX, :]

                # imgplot = plt.imshow(startingPoint)
                # plt.show()
                knownTileX, knownTileY, file = findShapes(1, startingPoint)
                fileRepo.append(file)
                # imgplot = plt.imshow(startingPoint)
                # plt.show()
                if knownTileX >= 0 and knownTileY >= 0:
                    tileEnum = findRightMapTileEnum(file)
                    if tileEnum != -1:
                        mapTile = MapTile(j, i, tileEnum)
                        world.appendMapTile(mapTile)
                    else:
                        print('Enum error')
    for repo in fileRepo:
        print(repo)
        # cv2.rectangle(im, (x, y), (x + tileSizeX, y + tileSizeY), (0, 0, 255), 5)

    print(world)

def findRightMapTileEnum(tileUrl):

    for e in mapTiles.MapTilesEnums:
        if e.value[1] == tileUrl:
            return e

    return -1

def getPlayerName(fileName):
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # image = cv2.imread(fileName)
    # image = image[195:215, 0:150, :]
    # img = Image.fromarray(image, 'RGB')
    # text = pytesseract.image_to_string(img, lang='eng')
    text = 'TEST'
    print(text)
    newPlayer = Player(text)
    world.appendPlayer(newPlayer)
    # plt.figure()
    # plt.imshow(image)
    # plt.show()

def createCity(x,y):

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
    newCity = cities.city(newCityName, x, y, world.getPlayerCivilization())
    world.getPlayerCivilization().addNewCity(newCity)
    world.getTileOnCords(x, y)

mode = 1
cordX, cordY = 0, 0
if mode == 0:
    click(findAllWindows())
    createSSBuffor(findAllWindows())
    # mode = 2
if mode == 1:
    cordX, cordY = findShapes(0)
    analyzeStartingPosition(cordX, cordY)
if mode == 2:
    click(findAllWindows())
    createSSBuffor(findAllWindows())
    createCity(cordX, cordY)
    # print(world)
