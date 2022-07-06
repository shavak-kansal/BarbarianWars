import string
import time
from os import system
import os
import sys
from telnetlib import GA
from colorama import init, Fore, Back, Style
import termios
import tty
import signal
import colorama
import numpy as np

from src.Building import *
from src.World import *
from src.input import *
from src.Moving import *

init()

if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]


def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()


hide_cursor()


def printPos(x, y, text_to_print):  # Function that let us print in desired Position
    sys.stdout.write("\x1b[%d;%df%s" % (x, y, text_to_print))


inputThing = Get()

starttime = time.time()

def kingHealthBar(world):
    bar = ''

    cnt = world.King.health // 10

    for i in range(int(cnt)):
        bar += '█'

    ret = " King Health: " + bar

    return ret

class GameLevel :
    def __init__(self, playerChoice) -> None:
        self.levelWorld = World(48, 48, playerChoice)
        self.barbarianSpawned = 0
        self.archerSpawned = 0
        self.balloonSpawned = 0
        self.playerChoice = playerChoice

    def level1(self) -> None:
        self.levelWorld.addTownHall(22, 23)
        self.levelWorld.addCannon(18, 23)
        self.levelWorld.addCannon(27, 23)
        
        self.levelWorld.addHut(27, 19)
        self.levelWorld.addHut(23, 19)
        self.levelWorld.addHut(19, 19)

        self.levelWorld.addHut(27, 27)
        self.levelWorld.addHut(23, 27)
        self.levelWorld.addHut(19, 27)

        self.levelWorld.addHut(21, 11)
        self.levelWorld.addHut(25, 11)
        self.levelWorld.addWizardTower(22, 14)

        self.levelWorld.addHut(18, 14)
        self.levelWorld.addHut(28, 14)

        self.levelWorld.addWizardTower(22, 31)
        self.levelWorld.addHut(18, 31)
        self.levelWorld.addHut(28, 31)

        self.genBottomWallGeneral(24, 23, 20, 15)
        self.genTopWallGeneral(24, 23, 20, 15)

        self.genLeftWallGeneral(24, 23, 30, 10)
        self.genRightWallGeneral(24, 23, 30, 10)

    def level2(self) -> None:
        self.levelWorld.addTownHall(22, 23)

        self.genBottomWallGeneral(24, 23, 20, 15)
        self.genTopWallGeneral(24, 23, 20, 15)
        self.genLeftWallGeneral(24, 23, 30, 10)
        self.genRightWallGeneral(24, 23, 30, 10)

        self.levelWorld.addCannon(18, 23)
        self.levelWorld.addCannon(27, 23)
        self.levelWorld.addWizardTower(22, 26)
        self.levelWorld.addWizardTower(22, 19)
        self.levelWorld.addWizardTower(18, 15)
        self.levelWorld.addCannon(27, 26)
        self.levelWorld.addHut(23, 16)
        self.levelWorld.addHut(27, 17)
        self.levelWorld.addHut(27, 20)
        self.levelWorld.addHut(19, 19)
        self.levelWorld.addHut(23, 13)
        self.levelWorld.addHut(18, 27)

    def level3(self) -> None:
        self.levelWorld.addTownHall(22, 23)

        self.genBottomWallGeneral(24, 23, 20, 15)
        self.genTopWallGeneral(24, 23, 20, 15)
        self.genLeftWallGeneral(24, 23, 30, 10)
        self.genRightWallGeneral(24, 23, 30, 10)

        self.levelWorld.addCannon(18, 23)
        self.levelWorld.addCannon(27, 23)
        self.levelWorld.addCannon(20, 26)
        self.levelWorld.addCannon(25, 20)

        self.levelWorld.addWizardTower(24, 26)
        self.levelWorld.addWizardTower(20, 19)
        self.levelWorld.addWizardTower(22, 15)
        self.levelWorld.addWizardTower(22, 30)

        self.levelWorld.addHut(19, 16)
        self.levelWorld.addHut(27, 17)
        self.levelWorld.addHut(19, 29)
        self.levelWorld.addHut(27, 30)
        self.levelWorld.addHut(29, 26)
        self.levelWorld.addHut(17, 26)
        self.levelWorld.addHut(17, 20)
        self.levelWorld.addHut(29, 20)
        self.levelWorld.addHut(27, 14)


    def genLeftWallGeneral(self, x: int, y: int, height: int, dist: int):
        for i in range(y-height//2, y + height//2):
            self.levelWorld.addWall(x - dist, i)


    def genRightWallGeneral(self, x: int, y: int, height: int, dist: int):
        for i in range(y-height//2, y + height//2):
            self.levelWorld.addWall(x + dist-1, i)


    def genTopWallGeneral(self, x: int, y: int, width: int, dist: int):
        for i in range(x- width//2, x + width//2):
            self.levelWorld.addWall(i, y - dist)


    def genBottomWallGeneral(self, x: int, y: int, width: int, dist: int):
        for i in range(x-width//2, x + width//2):
            self.levelWorld.addWall(i, y + dist-1)
    
    def clearLevel(self):
        self.levelWorld = World(48, 48, self.playerChoice)
        self.barbarianSpawned = 0
        self.archerSpawned = 0
        self.balloonSpawned = 0

class GameLoop():
    def __init__(self, playerChoice = 1) -> None:
        self.starttime = time.time()
        self.realWorldTimer = time.time()
        self.realWorldTime = 0 # world time in seconds 
        self.lastPlayerAttack = -1
        self.lastRage = -1
        self.GameLevel = GameLevel(playerChoice)
        self.GameLevel.level1()
        self.player = self.GameLevel.levelWorld.King
        self.inputThing = Get()
        self.level = 1
        self.inputList = []
        self.playerChoice = playerChoice
        self.queenQeuedTime = -1

    def inputHandler(self, input):
        
        if input == 'w':
            self.player.Move(0, self.GameLevel.levelWorld)
            self.GameLevel.levelWorld.updateRender()
            self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'a':
            self.player.Move(3, self.GameLevel.levelWorld)
            self.GameLevel.levelWorld.updateRender()
            self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 's':
            self.player.Move(2, self.GameLevel.levelWorld)
            self.GameLevel.levelWorld.updateRender()
            self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'd':
            self.player.Move(1, self.GameLevel.levelWorld)
            self.GameLevel.levelWorld.updateRender()
            self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'z':
            if self.GameLevel.barbarianSpawned < 6:
                self.GameLevel.levelWorld.addBarbarian(2,2)
                self.GameLevel.levelWorld.updateRender()
                self.GameLevel.barbarianSpawned +=1 
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'x':
            if self.GameLevel.barbarianSpawned < 6:
                self.GameLevel.levelWorld.addBarbarian(40,2)
                self.GameLevel.levelWorld.updateRender()
                self.GameLevel.barbarianSpawned +=1 
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'c':
            if self.GameLevel.barbarianSpawned < 6:
                self.GameLevel.levelWorld.addBarbarian(2,40)
                self.GameLevel.levelWorld.updateRender()
                self.GameLevel.barbarianSpawned +=1 
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'v':
            if self.GameLevel.archerSpawned < 6:
                self.GameLevel.levelWorld.addArcher(2,2)
                self.GameLevel.levelWorld.updateRender()
                self.GameLevel.archerSpawned +=1 
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")

        elif input == 'b':
            if self.GameLevel.archerSpawned < 6:
                self.GameLevel.levelWorld.addArcher(40,2)
                self.GameLevel.levelWorld.updateRender()
                self.GameLevel.archerSpawned +=1
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")

        elif input == 'n':
            if self.GameLevel.archerSpawned < 6:
                self.GameLevel.levelWorld.addArcher(2,40)
                self.GameLevel.levelWorld.updateRender()
                self.GameLevel.archerSpawned +=1 
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'j':
            if self.GameLevel.balloonSpawned < 3:
                self.GameLevel.levelWorld.addBalloon(2,2)
                self.GameLevel.levelWorld.updateRender()
                self.GameLevel.balloonSpawned += 1
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'k':
            if self.GameLevel.balloonSpawned < 3:
                self.GameLevel.levelWorld.addBalloon(40,2)
                self.GameLevel.levelWorld.updateRender()
                self.GameLevel.balloonSpawned += 1
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'l':
            if self.GameLevel.balloonSpawned < 3:
                self.GameLevel.levelWorld.addBalloon(2,40)
                self.GameLevel.levelWorld.updateRender()
                self.GameLevel.balloonSpawned += 1
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'r':
            if self.realWorldTime -self.lastRage > 10:
                Moving.movementSpeed = 2
                self.lastRage = self.realWorldTime
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")

        elif input == 'q':
            self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
            print(Style.RESET_ALL)
            system('clear')
            sys.exit()
        elif input == ' ':
            if self.realWorldTime - self.lastPlayerAttack > 1:
                self.player.attack(self.GameLevel.levelWorld)
                self.lastPlayerAttack = self.realWorldTime
                self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        elif input == 'h':
            for barbarian in self.GameLevel.levelWorld.barbarians:
                barbarian.health = min(barbarian.health*1.5, 100)

            for archer in self.GameLevel.levelWorld.archers:
                archer.health = min(archer.health*1.5, 50)
            
            for balloon in self.GameLevel.levelWorld.balloons:
                balloon.health = min(balloon.health*1.5, 100)

            if self.playerChoice == 1:
                self.player.health = min(self.player.health*1.5, 500)
            elif self.playerChoice == 2:
                self.player.health = min(self.player.health*1.5, 200)

            self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
        
        elif input == 'p':
            if self.playerChoice == 1:
                if self.realWorldTime - self.lastPlayerAttack > 1:
                    self.player.doAOE(self.GameLevel.levelWorld)
                    self.lastPlayerAttack = self.realWorldTime
                    self.inputList.append(input + ":" +str(self.realWorldTime) + ".")
            elif self.playerChoice == 2:
                if self.realWorldTime - self.lastPlayerAttack > 1:
                    self.queenQeuedTime = self.realWorldTimer
                    self.lastPlayerAttack = self.realWorldTime
                    self.inputList.append(input + ":" +str(self.realWorldTime) + ".")

        
    def runGame(self):
        x = 0
        
        lastUpdateirl = 0

        while True:
            
            if(time.time() - starttime > 1):
                printPos(2, 1, "                                                                                                                                                                                                            ")
                printPos(2, 1, "fps : " + str(x//((time.time() - starttime))) + " real world time : " + str(self.realWorldTime) + kingHealthBar(self.GameLevel.levelWorld))
                pass
            x += 1

            #system('clear')

            self.GameLevel.levelWorld.render()

            inp = input_to(inputThing, 0.0166)

            self.inputHandler(inp)

            if ((time.time() - self.realWorldTimer) > 1):
                self.realWorldTimer = time.time()
                self.realWorldTime += 1

                if self.realWorldTime - self.lastRage > 8:
                    Moving.movementSpeed = 1

                if self.queenQeuedTime != -1 :
                    if self.realWorldTimer - self.queenQeuedTime >= 1:
                        self.queenQeuedTime = -1
                        self.player.doAOE(self.GameLevel.levelWorld)

            if(self.realWorldTime > lastUpdateirl):
                lastUpdateirl = self.realWorldTime
                self.GameLevel.levelWorld.updateWorldState()
                self.GameLevel.levelWorld.updateRender()   
            
            if (self.GameLevel.levelWorld.Over == True):
                
                if (self.level == 1) and self.GameLevel.levelWorld.finishMsg == 'WON':
                    self.level = 2
                    self.GameLevel.clearLevel()
                    self.GameLevel.level2()
                    self.player = self.GameLevel.levelWorld.King
                    self.GameLevel.levelWorld.updateRender()
                elif (self.level == 2)  and self.GameLevel.levelWorld.finishMsg == 'WON':
                    self.level = 3
                    self.GameLevel.clearLevel()
                    self.GameLevel.level3()
                    self.player = self.GameLevel.levelWorld.King
                    self.GameLevel.levelWorld.updateRender()
                elif (self.level == 3)  and self.GameLevel.levelWorld.finishMsg == 'WON':
                    print(Style.RESET_ALL)
                    system('clear')
                    print("GAME FINISHED - " + self.GameLevel.levelWorld.finishMsg)
                    time.sleep(3)

                    with open('replays/replays.txt', 'a') as f:
                        for item in self.inputList:
                            f.write("%s" % item)
                        f.write('\n')

                        if(self.GameLevel.levelWorld.finishMsg == "WON"):
                            f.write("W")
                        else:
                            f.write("L")

                        f.write('\n')

                        f.write(str(self.playerChoice))
                        f.write('\n')

                    break

                elif self.GameLevel.levelWorld.finishMsg == 'LOST':
                    print(Style.RESET_ALL)
                    system('clear')
                    print("GAME FINISHED - " + self.GameLevel.levelWorld.finishMsg)
                    time.sleep(3)

                    with open('replays/replays.txt', 'a') as f:
                        for item in self.inputList:
                            f.write("%s" % item)
                        f.write('\n')

                        if(self.GameLevel.levelWorld.finishMsg == "WON"):
                            f.write("W")
                        else:
                            f.write("L")

                        f.write('\n')

                        f.write(str(self.playerChoice))
                        f.write('\n')

                    break
        
playerChoice = input("Enter your choice: 1. King 2. Archer Queen")

if playerChoice == '1':
    Game = GameLoop(1)
elif playerChoice == '2':
    Game = GameLoop(2)    

Game.runGame()
