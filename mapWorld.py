class MapWorld:

    def __init__(self):
        self.mapTiles = []
        self.playersAlive = []
        self.playersDead = []

    def appendMapTile(self, newTile):
        self.mapTiles.append(newTile)
