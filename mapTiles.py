from enum import Enum


class MapTiles:

    def __init__(self, tileName, tileImage, food, prod, trade, moveCost, defense):
        self.tileName = tileName
        self.tileImage = tileImage
        self.food = food
        self.prod = prod
        self.trade = trade
        self.moveCost = moveCost
        self.defense = defense

class MapTilesEnums(Enum):

    PLAINS_0 = ('Plains_0', 'aplains_0.png', 1, 1, 0, 1, 0)
    PLAINS_1 = ('Plains_1', 'aplains_1.png', 1, 2, 0, 1, 0)
    GRASSLAND_0 = ('Grassland_0', 'grassland_0.png', 2, 0, 0, 1, 0)
    GRASSLAND_1 = ('Grassland_1', 'grassland_1.png', 2, 1, 0, 1, 0)
    FOREST_0 = ('Forest_0', 'forest_0.png', 1, 2, 0, 2, 50)
    FOREST_1 = ('Forest_1', 'forest_1.png', 2, 2, 0, 2, 50)
    DESERT_0 = ('Desert_0', 'desert_0.png', 0, 1, 0, 1, 0)
    DESERT_1 = ('Desert_1', 'desert_1.png', 0, 1, 0, 1, 0)
    DESERT_2 = ('Desert_0', 'desert_2.png', 0, 1, 0, 1, 0)
    OCEAN_0 = ('Ocean_0', 'ocean_0.png', 1, 0, 2, 1, 0)
    OCEAN_1 = ('Ocean_1', 'ocean_1.png', 1, 2, 2, 1, 0)
    OCEAN_2 = ('Ocean_0', 'ocean_2.png', 1, 0, 2, 1, 0)
    OCEAN_3 = ('Ocean_0', 'ocean_3.png', 1, 0, 2, 1, 0)
    OCEAN_4 = ('Ocean_0', 'ocean_4.png', 1, 0, 2, 1, 0)
    OCEAN_5 = ('Ocean_0', 'ocean_5.png', 1, 0, 2, 1, 0)
    OCEAN_6 = ('Ocean_0', 'ocean_6.png', 1, 0, 2, 1, 0)
    LAKE = ('Ocean_0', 'lake_0.png', 1, 0, 2, 1, 0)
    HILLS_0 = ('Hills_0', 'hills_0.png', 1, 0, 0, 2, 100)
    HILLS_1 = ('Hills_1', 'hills_1.png', 1, 2, 0, 2, 100)
    HILLS_3 = ('Hills_0', 'hills_3.png', 1, 0, 0, 2, 100)
    HILLS_4 = ('Hills_0', 'hills_4.png', 1, 0, 0, 2, 100)
    HILLS_5 = ('Hills_0', 'hills_5.png', 1, 0, 0, 2, 100)
    RIVER_0 = ('River_0', 'river_0.png', 2, 0, 1, 1, 50)
    RIVER_4 = ('River_0', 'river_4.png', 2, 0, 1, 1, 50)
    RIVER_5 = ('River_0', 'river_5.png', 2, 0, 1, 1, 50)
    RIVER_6 = ('River_0', 'river_6.png', 2, 0, 1, 1, 50)
    RIVER_7 = ('River_0', 'river_7.png', 2, 0, 1, 1, 50)
    RIVER_8 = ('River_0', 'river_8.png', 2, 0, 1, 1, 50)
    RIVER_9 = ('River_0', 'river_9.png', 2, 0, 1, 1, 50)
    SWAMP_0 = ('Swamp_0', 'swamp_0.png', 1, 0, 0, 2, 50)

    UNKNOWN = ('Uknown', 'uknown.png', 0, 0, 0, 0, 0)
