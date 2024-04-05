class MapTile:

    def __init__(self, cordX, cordY, tile):
        self.cordX = cordX
        self.cordY = cordY
        self.tile = tile
        self.city = False
        self.cityName = ''
        self.units = []

    def getCords(self):
        return self.cordX, self.cordY

    def getTileFundation(self):
        return self.tile