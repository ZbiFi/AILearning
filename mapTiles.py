from enum import Enum


class MapTiles:

    def __init__(self, tileName, tileImage):
        self.tileName = tileName
        self.tileImage = tileImage
        self.food = 0
        self.prod = 0
        self.trade = 0

class MapTilesEnums(Enum):

    GRASSLAND_0 = ('Grassland_0', 'grassland_0.png')