import numpy as np
from colorama import init, Fore, Back, Style

class Building ():
    def __init__(self, x, y, width, height, health, color, name, type):
        self.X = x  # TOP LEFT CORNER X COORDINATE
        self.Y = y  # TOP LEFT CORNER Y COORDINATE
        self.width = width
        self.height = height
        self.health = health
        self.color = color
        self.identifier = name
        self.type = type # 1 for king

    def __str__(self) -> str:
        return "Building at ({},{}) with width {} and height {} and health {}".format(self.X, self.Y, self.width, self.height, self.health)

    def render(self) -> str:     
        ret1 = [['' for i in range(self.width)] for j in range(self.height)]

        ret1[0][0] = '╔'
        ret1[0][self.width-1] = '╗'
        ret1[self.height-1][0] = '╚'
        ret1[self.height-1][self.width-1] = '╝'

        for i in range(1, self.width-1):
            ret1[0][i] = '='
            ret1[self.height-1][i] = '='

        for i in range(1, self.height-1):
            ret1[i][0] = '║'
            ret1[i][self.width-1] = '║'

        for i in range(1, self.width-1):
            for j in range(1, self.height-1):
                ret1[j][i] = self.identifier

        if self.width == 1 and self.height == 1:
            ret1[0][0] = self.identifier

        return ret1

    def updateState(self, world):
        
        if(self.health > 50  and self.health < 100):
            self.color = Fore.GREEN
        elif(self.health > 20 and self.health < 50):
            self.color = Fore.YELLOW
        elif(self.health > 0 and self.health < 20):
            self.color = Fore.RED
        elif(self.health <= 0):
            return 1

    def colorUpdate(self):  # update color of building according to health
        if(self.health > 50  and self.health < 100):
            self.color = Fore.GREEN
        elif(self.health > 20 and self.health < 50):
            self.color = Fore.YELLOW
        elif(self.health > 0 and self.health < 20):
            self.color = Fore.RED
        elif(self.health <= 0):
            return 1

    def checkCollision(self, other):
        if abs((self.X + self.width/2) - (other.X + other.width/2)) >= (self.width/2 + other.width/2):
            return False
        if abs((self.Y + self.height/2) - (other.Y + other.height/2)) >= (self.height/2 + other.height/2):
            return False

        return True

class Wall(Building):
    def __init__(self, x, y, health):
        super().__init__(x, y, 1, 1, health, Fore.GREEN, 'X', -1)

    def __str__(self) -> str:
        return "Wall at ({},{}) with width {} and height {} and health {}".format(self.X, self.Y, self.width, self.height, self.health)

    def render(self): 
        ret = [[self.identifier for i in range(1)] for j in range(1)]
        return ret

class TownHall(Building):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, 4, 3, health, Fore.GREEN, 'T', -2)

    def __str__(self) -> str:
        return "TownHall at ({},{}) with width {} and height {} and health {}".format(self.X, self.Y, self.width, self.height, self.health)

class Hut(Building):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, 2, 3, health, Fore.GREEN, 'H', -4)

    def __str__(self) -> str:
        return "Hut at ({},{}) with width {} and height {} and health {}".format(self.X, self.Y, self.width, self.height, self.health)

    def render(self):
        ret = [['╔', '╗'],['H','H'],['╚', '╝'] ]
        return ret

class Cannon(Building):
    def __init__(self, x, y, health = 100, damage=10, range=10):
        super().__init__(x, y, 3, 3, health, Fore.GREEN, 'C', -3)
        self.damage = damage
        self.range = range
        self.target = None

    def updateState(self, world):
        self.colorUpdate()

        if self.health <= 0:
            return 1
             
        if self.target is None:
            for index, building in enumerate(world.buildings):
                if building.type == 1 and building.damage!=40:
                    if (building.X - self.X)**2 + (building.Y - self.Y)**2 <= self.range**2:
                        self.target = building
        else : 
            if (self.target.X - self.X)**2 + (self.target.Y - self.Y)**2 <= self.range**2:
                if self.target.health <= 0:
                    self.target = None
                else:
                    self.target.health -= self.damage
                    sth = self.target.color
                    self.target.color = self.target.swapColor
                    self.target.swapColor = sth
            else :
                self.target = None

    def __str__(self) -> str:
        return "Cannon at ({},{}) with width {} and height {} and health {}".format(self.X, self.Y, self.width, self.height, self.health)

class WizardTower(Building):
    def __init__(self, x, y, health = 100, damage=10, range=10):
        super().__init__(x, y, 4, 4, health, Fore.GREEN, 'W', -5)
        self.damage = damage
        self.range = range
        self.target = None

    def findTarget(self, world):
        for index, building in enumerate(world.buildings):
            if building.type == 1:
                if (building.X - self.X)**2 + (building.Y - self.Y)**2 <= self.range**2:
                    self.target = building

    def updateState(self, world):
        self.colorUpdate()

        if self.health <= 0:
            return 1
             
        if self.target is None:
            for index, building in enumerate(world.buildings):
                if building.type == 1:
                    if (building.X - self.X)**2 + (building.Y - self.Y)**2 <= self.range**2:
                        self.target = building
                        #print("Target is {} with color {} A".format(self.target, self.target.color))
        else : 
            print("Target is {}".format(self.target))
            
            if self.target.health <= 0:
                self.target = None
                
            elif (self.target.X - self.X)**2 + (self.target.Y - self.Y)**2 <= self.range**2:
                for index, building in enumerate(world.buildings):
                    if building.type == 1:
                        #if (building.X - self.X)**2 + (building.Y - self.Y)**2 <= self.range**2:
                        if abs(building.X - self.target.X) < 2 and abs(building.Y - self.target.Y) < 2:
                            building.health -= self.damage
                            sth = building.color
                            building.color = building.swapColor
                            building.swapColor = sth
            else :
                self.target = None

