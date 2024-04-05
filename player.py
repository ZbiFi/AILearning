class Player:

    def __init__(self, name):
        self.playerName = name
        self.color = ''
        self.cities = []
        self.units = []
        self.wealth = 0
        self.science = 0
        self.goverment = None
        self.score = 0


    def getCities(self):
        return self.cities

    def addNewCity(self, city):

        self.cities.append()