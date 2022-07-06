import enum
from src.Building import *
from src.Moving import *

import sys

def printPos(x, y, text_to_print):   #Function that let us print in desired Position
    sys.stdout.write("\x1b[%d;%df%s" % (x, y, text_to_print))
    #sys.stdout.flush()

class World :
    def __init__(self, sizeWidth, sizeHeight, choice = 1):
        self.sizeWidth = sizeWidth
        self.sizeHeight = sizeHeight
        self.buildings = []
        self.barbarians = []
        self.archers = []
        self.balloons = []
        self.huts = []
        self.canons = []
        self.wizardTowers = []
        self.townhall = None
        self.Over = False
        self.finishMsg = ''

        if choice == 1 :
            self.King = King(2, 2)
        elif choice == 2 :
            self.King = ArcherQueen(2, 2)

        self.buildings.append(self.King)

        self.Display = ''

        
    def addTownHall(self, x, y):
        #self.buildings.append(TownHall(x, y, 100))
        townhall = TownHall(x, y, 100)
        self.townhall = townhall
        self.buildings.append(townhall)

    def addCannon(self, x, y, damage=10, range=10):
        canon = Cannon(x, y, 100, damage, range)
        self.buildings.append(canon)
        self.canons.append(canon)

    def addWall(self, x, y):
        wall = Wall(x, y, 100)
        self.buildings.append(wall)
        
    def addHut(self, x, y):
        hut = Hut(x, y, 100)
        self.buildings.append(hut)
        self.huts.append(hut)

    def addWizardTower(self, x, y):
        wiz = WizardTower(x, y, 100)
        self.buildings.append(wiz)
        self.wizardTowers.append(wiz)

    def addBarbarian(self, x, y, damage=20):
        barbarian = Barbarian(x, y)
        self.buildings.append(barbarian)
        self.barbarians.append(barbarian)
    
    def addArcher(self, x, y, damage=10):
        archer = Archer(x, y)
        self.buildings.append(archer)
        self.archers.append(archer)

    def addBalloon(self, x, y, damage=40):
        balloon = Balloon(x, y, 100, damage)
        self.buildings.append(balloon)
        self.balloons.append(balloon)

    def updateWorldState(self):
        for index, building in enumerate(self.buildings):
            # res = building.updateState(self)
            # if res == 1:
            #     self.buildings.pop(index)
            if building.type != 1:
                building.colorUpdate()
                if building.health <= 0 :
                    self.buildings.pop(index)
            else :
                if building.health <= 0 :
                    self.buildings.pop(index)



        for index, hut in enumerate(self.huts):
            res = hut.updateState(self)
            if res == 1:
                self.huts.pop(index)
        
        
        for index, canon in enumerate(self.canons):
            res = canon.updateState(self)
            if res == 1:
                self.canons.pop(index)
        
        for index, wizard in enumerate(self.wizardTowers):
            res = wizard.updateState(self)
            if res == 1:
                self.wizardTowers.pop(index)

        for index, barbarian in enumerate(self.barbarians):
            res = barbarian.updateState(self)
            if res == 1:
                self.barbarians.pop(index)

        for index, archer in enumerate(self.archers):
            res = archer.updateState(self)
            if res == 1:
                self.archers.pop(index)
        
        for index, balloon in enumerate(self.balloons):
            res = balloon.updateState(self)
            if res == 1:
                self.balloons.pop(index)

        if self.townhall is not None :
            res = self.townhall.updateState(self)
            if res == 1:
                self.townhall = None
                
            
        if self.townhall is None and len(self.huts) == 0 and len(self.canons) == 0 and len(self.wizardTowers) == 0:
            self.Over = True
            self.finishMsg = 'WON'
        
        if self.King.health <= 0 :
            self.Over = True
            self.finishMsg = 'LOST'
            
    def updateRender(self):
        matr = np.full((self.sizeHeight, self.sizeWidth), ' ', dtype=np.unicode_)
        matrixId = np.full((self.sizeHeight, self.sizeWidth), -1, dtype=int)

        finalScreen = ''

        for index, building in enumerate(self.buildings):
            buildStr = building.render()
            
            for i in range(len(buildStr)):
                for j in range(len(buildStr[i])):
                    matr[building.Y + i][building.X + j] = buildStr[i][j]
                    matrixId[building.Y + i][building.X + j] = index

        for i in range(self.sizeHeight):
            index1 = 0
            index2 = 0

            while index1 < self.sizeWidth and index2 < self.sizeWidth:
                if matrixId[i][index1] == matrixId[i][index2]:
                    index2 += 1
                else:
                    if (matrixId[i][index1] != -1):
                        finalScreen += self.buildings[matrixId[i][index1]].color

                    if(matrixId[i][index1] == -2):
                        finalScreen += self.Player.color

                    for j in range(index1, index2):
                        finalScreen += matr[i][j]

                    index1 = index2

            if index1 < self.sizeWidth and index2 == self.sizeWidth :
                
                if (matrixId[i][index1] != -1):
                    finalScreen += self.buildings[matrixId[i][index1]].color

                if(matrixId[i][index1] == -2):
                        finalScreen += self.Player.color

                for j in range(index1, index2):
                    finalScreen += matr[i][j]

            finalScreen += '\n'

        self.Display = finalScreen

    def render(self):
        printPos(3, 0, self.Display)

    def addPlayer(self, player):
        self.Player = player
        self.buildings.append(player)
        
    def oldrender(self):
        ret = [[' ' for i in range(self.sizeWidth)] for j in range(self.sizeHeight)]
        colorArr = [[' ' for i in range(self.sizeWidth)] for j in range(self.sizeHeight)]

        finalScreen = ''

        for building in self.buildings:
            buildStr = building.render()
            
            for i in range(len(buildStr)):
                for j in range(len(buildStr[i])):
                    ret[building.X + i][building.Y + j] = buildStr[i][j] 
                    colorArr[building.X + i][building.Y + j] = building.color

        ret[self.Player.Y][self.Player.X] = 'P'

        for i in range(len(ret)):
            finalScreen += ''.join(ret[i]) + '\n'
        
        printPos(3, 0, finalScreen)
