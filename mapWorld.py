class MapWorld:

    def __init__(self):
        self.mapTiles = []
        self.playersAlive = []
        self.playersDead = []

    def appendMapTile(self, newTile):
        self.mapTiles.append(newTile)

    def appendPlayer(self, newPlayer):
        self.playersAlive.append(newPlayer)

    def removePlayer(self, removedPlayer):
        self.playersAlive.remove(removedPlayer)
        self.playersDead.append(removedPlayer)

    def getPlayerCivilization(self):
        return self.playersAlive[0]

    def getTileOnCords(self, x, y):

        for tile in self.mapTiles:
            if tile.getCords() == (x, y):
                return tile.getTileFundation()