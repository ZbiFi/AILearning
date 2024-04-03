from enum import Enum


class MapTiles:

    def __init__(self, tileName, tileImage):
        self.tileName = tileName
        self.tileImage = tileImage
        self.food = 0
        self.prod = 0
        self.trade = 0

class MapTilesEnums(Enum):

    PLAINS_0 = ('Plains_0', 'aplains_0.png')
    PLAINS_1 = ('Plains_1', 'aplains_1.png')
    GRASSLAND_0 = ('Grassland_0', 'grassland_0.png')
    GRASSLAND_1 = ('Grassland_1', 'grassland_1.png')
    FOREST_0 = ('Forest_0', 'forest_0.png')
    FOREST_1 = ('Forest_1', 'forest_1.png')