from ctypes.wintypes import WORD
import imp
from src.Building import *
from colorama import init, Fore, Back, Style

#import World
import math

class Moving(Building):
    """
    Class to represent a moving object.
    """

    movementSpeed = 1

    def __init__(self, x, y, width, height, health, color, name, type = 1):
        """
        Initializes the moving object.

        :param x: x coordinate of the moving object.
        :param y: y coordinate of the moving object.
        """
        super().__init__(x, y, width, height, health, color, name, type)
        self.swapColor = Fore.WHITE
        self.baseSpeed = 1

    def move(self, world, dx, dy):
        """
        Moves the object.

        :param width: width of the screen.
        :param height: height of the screen.
        """
        xLeft = dx 
        yLeft = dy

        inWay = None

        while xLeft != 0 or yLeft != 0:
            
            if xLeft > 0:
                self.X += 1
                xLeft -= 1

                if self.checkInWay(world) is not None:
                    inWay = self.checkInWay(world)
                    self.X -= 1
                    xLeft = 0
                
                if self.X > world.sizeWidth - 1:
                    self.X = world.sizeWidth - 1
                    xLeft = 0

            elif xLeft < 0:
                self.X -= 1
                xLeft += 1
                
                if self.checkInWay(world) is not None:
                    inWay = self.checkInWay(world)
                    self.X += 1
                    xLeft = 0

                if self.X < 0:
                    self.X = 0
                    xLeft = 0

                
            
            if yLeft > 0:
                self.Y += 1
                yLeft -= 1

                if self.checkInWay(world) is not None:
                    inWay = self.checkInWay(world)
                    self.Y -= 1
                    yLeft = 0
                
                if self.Y > world.sizeHeight - 1:
                    self.Y = world.sizeHeight - 1
                    yLeft = 0

                

            elif yLeft < 0:
                self.Y -= 1
                yLeft += 1

                if self.checkInWay(world) is not None:
                    inWay = self.checkInWay(world)
                    self.Y += 1
                    yLeft = 0

                if self.Y < 0:
                    self.Y = 0
                    yLeft = 0

        return inWay

    def checkOverlap(self, world):
        for building in world.buildings:
            if building.type != 1:
                if abs((self.X + self.width/2) - (building.X + building.width/2)) >= (self.width/2 + building.width/2):
                    continue
                if abs((self.Y + self.height/2) - (building.Y + building.height/2)) >= (self.height/2 + building.height/2):
                    continue

                return True

        return False

    def checkInWay(self, world):
        for building in world.buildings:
            if building.type != 1:
                if abs((self.X + self.width/2) - (building.X + building.width/2)) >= (self.width/2 + building.width/2):
                    continue
                if abs((self.Y + self.height/2) - (building.Y + building.height/2)) >= (self.height/2 + building.height/2):
                    continue

                return building

        return None
    
    def updateState(self, world):
        return 0

    def distanceFromBuilding(self, building : Building):
        #return math.sqrt((self.X - building.X)**2 + (self.Y - building.Y)**2)

        dist = (self.X - building.X)**2 + (self.Y - building.Y)**2

        if (self.X - (building.X + building.width))**2 + (self.Y - (building.Y + building.height))**2 < dist:
            dist = (self.X - (building.X + building.width))**2 + (self.Y - (building.Y + building.height))**2

        if (self.X - (building.X + building.width))**2 + (self.Y - building.Y)**2 < dist:
            dist = (self.X - (building.X + building.width))**2 + (self.Y - building.Y)**2

        if (self.X - building.X)**2 + (self.Y - (building.Y + building.height))**2 < dist:
            dist = (self.X - building.X)**2 + (self.Y - (building.Y + building.height))**2

        return math.sqrt(dist)

class King(Moving) :
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1, 500, Fore.MAGENTA, 'K')
        self.damage = 50

    def Move(self, dir, world):
        if dir == 0:
            super().move(world, 0, -1*Moving.movementSpeed)
        elif dir == 1:
            super().move(world, 1*Moving.movementSpeed, 0)
        elif dir == 2:
            super().move(world, 0, 1*Moving.movementSpeed)
        elif dir == 3:
            super().move(world, -1*Moving.movementSpeed, 0)

    def move(self, width, height, dx, dy, world):

        prevX = self.X
        prevY = self.Y

        super().move(world, dx, dy)

    def attack(self, world):
        self.doDamage(world)

    def doDamage(self, world):
        x = self.X+1
        y = self.Y

        for building in world.buildings:
            if building.type != 1:
                if abs((x + self.width/2) - (building.X + building.width/2)) >= (self.width/2 + building.width/2):
                    continue
                if abs((y + self.height/2) - (building.Y + building.height/2)) >= (self.height/2 + building.height/2):
                    continue

                building.health -= self.damage

    def doAOE(self, world):
        x = self.X
        y = self.Y

        for building in world.buildings:
            if building.type != 1:
                # if abs((x + 5) - (building.X + building.width/2)) > (5 + building.width/2):
                #     continue
                # if abs((y + 5) - (building.Y + building.height/2)) > (5 + building.height/2):
                #     continue
                if (x - building.X)**2 + (y - building.Y)**2 < 25:
                    building.health -= self.damage

class ArcherQueen(Moving) :
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1, 200, Fore.MAGENTA, 'Q')
        self.damage = 30
        self.lastDir = 0 # 0 for up 2 for down 3 for left 1 for right
    
    def attack(self, world):
        self.doDamage(world)

    def Move(self, dir, world):
        if dir == 0:
            super().move(world, 0, -1*Moving.movementSpeed)
            self.lastDir = 0
        elif dir == 1:
            super().move(world, 1*Moving.movementSpeed, 0)
            self.lastDir = 1
        elif dir == 2:
            super().move(world, 0, 1*Moving.movementSpeed)
            self.lastDir = 2
        elif dir == 3:
            super().move(world, -1*Moving.movementSpeed, 0)
            self.lastDir = 3

    def doDamage(self, world):
        centreX = self.X
        centreY = self.Y

        if self.lastDir == 0:
            centreY -= 8
        elif self.lastDir == 1:
            centreX += 8
        elif self.lastDir == 2:
            centreY += 8
        elif self.lastDir == 3:
            centreX -= 8
        
        for building in world.buildings:
            if building.type != 1:
                if abs(centreX - building.X) < 3 and abs(centreY - building.Y) < 3:
                    building.health -= self.damage

    def doAOE(self, world):
        centreX = self.X
        centreY = self.Y

        if self.lastDir == 0:
            centreY -= 16
        elif self.lastDir == 1:
            centreX += 16
        elif self.lastDir == 2:
            centreY += 16
        elif self.lastDir == 3:
            centreX -= 16
        
        for building in world.buildings:
            if building.type != 1:
                if abs(centreX - building.X) < 5 and abs(centreY - building.Y) < 5:
                    building.health -= self.damage

class Barbarian(Moving) :
    def __init__(self, x, y, health = 100, damage = 20):
        super().__init__(x, y, 1, 1, health, Fore.RED, 'B')
        self.target = None
        self.damage = damage
        self.aX = x
        self.aY = y

    def move(self, width, height, dx, dy, world):

        prevX = self.X
        prevY = self.Y

        inway = super().move(world, dx, dy)

        return inway

    def findClosestBuilding(self, world):
        closest = None
        closestDistance = 100000

        for hut in world.huts:
            distance = math.sqrt((self.X - hut.X)**2 + (self.Y - hut.Y)**2)
            if distance < closestDistance:
                closest = hut
                closestDistance = distance

        for canon in world.canons:
            distance = math.sqrt((self.X - canon.X)**2 + (self.Y - canon.Y)**2)
            if distance < closestDistance:
                closest = canon
                closestDistance = distance

        for wiz in world.wizardTowers :
            distance = math.sqrt((self.X - wiz.X)**2 + (self.Y - wiz.Y)**2)
            if distance < closestDistance:
                closest = wiz
                closestDistance = distance
        
        if world.townhall is not None :
            distance = math.sqrt((self.X - world.townhall.X)**2 + (self.Y - world.townhall.Y)**2)
            if distance < closestDistance:
                closest = world.townhall
                closestDistance = distance

        return closest

    def targetSelection (self, world):
        pass
    
    def updateState(self, world):
        if self.health <= 0 :
            return 1

        if self.target is None :
            ret = self.findClosestBuilding(world)

            if ret is not None:
                #print("Barbarian is moving to {}".format(ret))
                self.target = ret
            else :
                pass
        
        if self.target is not None:

            if abs((self.X + self.width/2) - (self.target.X + self.target.width/2)) <= (self.width/2 + self.target.width/2) and abs((self.Y + self.height/2) - (self.target.Y + self.target.height/2)) <= (self.height/2 + self.target.height/2):
                    self.target.health -= self.damage
            else :
                if self.target.X < self.X :
                    inWay = self.move(world.sizeWidth, world.sizeHeight, max(-1 * Moving.movementSpeed, - self.X + self.target.X), 0, world)
                elif self.target.X > self.X :
                    inWay = self.move(world.sizeWidth, world.sizeHeight, min(1 * Moving.movementSpeed, - self.X + self.target.X), 0, world)
                
                if self.target.Y < self.Y :
                    inWay = self.move(world.sizeWidth, world.sizeHeight, 0, max(-1 * Moving.movementSpeed, - self.Y + self.target.Y), world)
                elif self.target.Y > self.Y :
                    inWay = self.move(world.sizeWidth, world.sizeHeight, 0, min(1 * Moving.movementSpeed, - self.Y + self.target.Y), world)

                if self.target.health <= 0:
                    self.target = None
                    return 0
                
                if inWay is not None:
                    inWay.health -= self.damage
            
class Archer(Moving) :
    def __init__(self, x, y, health = 50, damage = 10):
        super().__init__(x, y, 1, 1, health, Fore.RED, 'A')
        self.target = None # target of archer in range
        self.closestTarget = None # closest target to the archer outside of his range
        self.damage = damage
        self.aX = x
        self.aY = y
        #Moving.movementSpeed = 2
        self.baseSpeed = 2
        self.range = 15

    def findTarget(self, world) :
        for canon in world.canons:
            if self.distanceFromBuilding(canon) <= self.range:
                self.target = canon
                return canon

        for hut in world.huts:
            if self.distanceFromBuilding(hut) <= self.range:
                self.target = hut
                return hut
        
        for wiz in world.wizardTowers :
            if self.distanceFromBuilding(wiz) <= self.range:
                self.target = wiz
                return wiz
        
        if world.townhall is not None :
            if self.distanceFromBuilding(world.townhall) <= self.range:
                self.target = world.townhall
                return world.townhall

        return None
    
    def attack(self):
        if self.target is not None:
            self.target.health -= self.damage

    def findClosestBuilding(self, world):
        closest = None
        closestDistance = 100000

        for hut in world.huts:
            if self.distanceFromBuilding(hut) < closestDistance:
                closest = hut
                closestDistance = self.distanceFromBuilding(hut)

        for canon in world.canons:
            if self.distanceFromBuilding(canon) < closestDistance:
                closest = canon
                closestDistance = self.distanceFromBuilding(canon)
        
        if world.townhall is not None :
            if self.distanceFromBuilding(world.townhall) < closestDistance:
                closest = world.townhall
                closestDistance = self.distanceFromBuilding(world.townhall)

        return closest
    
    def moveTowards(self, building : Building, world):
        inWay = None

        if building.X < self.X :
            inWay = self.move(world, max(-1 * Moving.movementSpeed * self.baseSpeed, - self.X + building.X), 0)
        elif building.X > self.X :
            inWay = self.move(world, min(1 * Moving.movementSpeed * self.baseSpeed, - self.X + building.X), 0)
        
        if building.Y < self.Y :
            inWay = self.move(world, 0, max(-1 * Moving.movementSpeed * self.baseSpeed, - self.Y + building.Y))
        elif building.Y > self.Y :
            inWay = self.move(world, 0, min(1 * Moving.movementSpeed * self.baseSpeed, - self.Y + building.Y))

        if inWay is not None:
            inWay.health -= self.damage
        
    def updateState(self, world):
        
        if self.health <= 0 :
            return 1

        if self.target is None :
            ret = self.findTarget(world)

            if ret is not None:
                self.target = ret
                self.closestTarget = None
            else:
                if self.closestTarget is not None:
                    self.moveTowards(self.closestTarget, world)
                else :
                    self.closestTarget = self.findClosestBuilding(world)

                    if self.closestTarget is not None:
                        self.moveTowards(self.closestTarget, world)
        else :
            if self.target.health <= 0:
                self.target = None
                return 0

            if self.distanceFromBuilding(self.target) <= self.range:
                self.attack()
            else :
                self.moveTowards(self.target, world)

    def __str__(self) -> str:
        return super().__str__() + " Archer"

class Balloon(Moving) :
    def __init__(self, x, y , health = 100, damage = 40):
        super().__init__(x, y, 1, 1, health, Fore.RED, 'L')
        self.target = None # closest target to the balloon
        self.damage = damage
        self.baseSpeed = 2
    
    def findTarget(self, world):
        closest = None
        closestDistance = 100000

        if len(world.wizardTowers) > 0 or len(world.canons) > 0:
            for tower in world.wizardTowers:
                if self.distanceFromBuilding(tower) < closestDistance:
                    closest = tower
                    closestDistance = self.distanceFromBuilding(tower)
            
            for canon in world.canons:
                if self.distanceFromBuilding(canon) < closestDistance:
                    closest = canon
                    closestDistance = self.distanceFromBuilding(canon)

            return closest
        else :
            for hut in world.huts:
                if self.distanceFromBuilding(hut) < closestDistance:
                    closest = hut
                    closestDistance = self.distanceFromBuilding(hut)
                    return closest

            if world.townhall is not None :
                if self.distanceFromBuilding(world.townhall) < closestDistance:
                    closest = world.townhall
                    closestDistance = self.distanceFromBuilding(world.townhall)
                    return closest

            return closest
    
    def updateState(self, world):
        if self.health <= 0 :
            return 1

        if self.target is None :
            self.target = self.findTarget(world)
        else :
            if self.target.health <= 0:
                self.target = None
                return 0

            #if self.distanceFromBuilding(self.target) <= self.range:
            if self.X == self.target.X and self.Y == self.target.Y:
                self.target.health -= self.damage
            else :
                self.moveTowards(self.target, world)
    
    def moveTowards(self, building : Building, world):

        if building.X < self.X :
            self.X -= min(1 * Moving.movementSpeed * self.baseSpeed, self.X - building.X)    
        elif building.X > self.X :
            self.X += min(1 * Moving.movementSpeed * self.baseSpeed, building.X - self.X)
        
        if building.Y < self.Y :
            self.Y -= min(1 * Moving.movementSpeed * self.baseSpeed, self.Y - building.Y)
        elif building.Y > self.Y :
            self.Y += min(1 * Moving.movementSpeed * self.baseSpeed, building.Y - self.Y)
