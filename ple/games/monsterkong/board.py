__author__ = 'Batchu Vishal'
import pygame
import math
import sys
import os
import numpy as np
from .person import Person
from .onBoard import OnBoard
from .coin import Coin
from .player import Player

class Board(object):
    '''
    This class defines our gameboard.
    A gameboard contains everthing related to our game on it like our characters, walls, ladders, coins etc
    The generation of the level also happens in this class.
    '''

    def __init__(self, width, height, rewards, rng, _dir):
        self.__width = width
        self.__actHeight = height
        self.__height = self.__actHeight + 10
        self.score = 0
        self.rng = rng
        self.rewards = rewards
        self.cycles = 0  # For the characters animation
        self.direction = 0
        self._dir = _dir
        self.IMAGES = {
            "still": pygame.image.load(os.path.join(_dir, 'assets/still.png')).convert_alpha(),
            "monster0": pygame.image.load(os.path.join(_dir, 'assets/monster0.png')).convert_alpha(),
            "princess": pygame.image.load(os.path.join(_dir, 'assets/princess.png')).convert_alpha(),
            "coin1": pygame.image.load(os.path.join(_dir, 'assets/spikes.png')).convert_alpha(),
            "wood_block": pygame.image.load(os.path.join(_dir, 'assets/wood_block.png')).convert_alpha(),
            "wood_block2": pygame.image.load(os.path.join(_dir, 'assets/wood_block2.png')).convert_alpha(),
            "wood_block3": pygame.image.load(os.path.join(_dir, 'assets/wood_block3.png')).convert_alpha(),
            "wood_block4": pygame.image.load(os.path.join(_dir, 'assets/wood_block4.png')).convert_alpha(),
            "wood_block5": pygame.image.load(os.path.join(_dir, 'assets/wood_block5.png')).convert_alpha(),
            "boundary": pygame.image.load(os.path.join(_dir, 'assets/boundary.png')).convert_alpha(),            
            "ladder": pygame.image.load(os.path.join(_dir, 'assets/ladder.png')).convert_alpha()
        }

        self.white = (255, 255, 255)

        '''
        The map is essentially an array of 30x80 in which we store what each block on our map is.
        1 represents a wall, 2 for a ladder and 3 for a coin.
        '''
        self.map = []
        # These are the arrays in which we store our instances of different
        # classes
        self.Players = []
        self.Allies = []
        self.Coins = []
        self.Walls = []
        self.Ladders = []
        self.Boards = []

        # Resets the above groups and initializes the game for us
        self.resetGroups()

        # Initialize the instance groups which we use to display our instances
        # on the screen
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.ladderGroup = pygame.sprite.RenderPlain(self.Ladders)
        self.coinGroup = pygame.sprite.RenderPlain(self.Coins)
        self.allyGroup = pygame.sprite.RenderPlain(self.Allies)

    def resetGroups(self):
        self.score = 0
        self.lives = 3
        self.map = []  # We will create the map again when we reset the game
        self.Players = [Player(self.IMAGES["still"],(100, 290),15,15)] #initial position of the player
        self.Allies = [Person(self.IMAGES["princess"], (50, 48), 18, 25)] #initial position of the goal i.e. princess
        self.Allies[0].updateWH(self.Allies[0].image, "H", 0, 25, 25)
        self.Coins = []
        self.Walls = []
        self.Ladders = []
        self.initializeGame()  # This initializes the game and generates our map
        self.createGroups()  # This creates the instance groups

    # Given a position and checkNo ( 1 for wall, 2 for ladder, 3 for coin) the
    # function tells us if its a valid position to place or not
    def checkMapForMatch(self, placePosition, floor, checkNo, offset):
        if floor < 1:
            return 0
        for i in range(
                0, 5):  # We will get things placed atleast 5-1 blocks away from each other
            if self.map[floor * 5 - offset][placePosition + i] == checkNo:
                return 1
            if self.map[floor * 5 - offset][placePosition - i] == checkNo:
                return 1
        return 0

    def populateMap(self):
        f = open ( 'map_short.txt' , 'r')
        self.map = [ map(int,line.split(',')) for line in f if line.strip() != "" ] #load your own custom map here
        
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 1:
                    # Add a wall at that position
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))
                elif self.map[x][y] == 2:
                    # Add a ladder at that position
                    self.Ladders.append(
                        OnBoard(
                            self.IMAGES["ladder"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))
                elif self.map[x][y] == 3:
                    # Add the coin to our coin list
                    self.Coins.append(
                        Coin(
                            self.IMAGES["coin1"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2),
                             self._dir))
                # Add a wall at that position
                elif self.map[x][y] == 4:
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block2"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))                 
                elif self.map[x][y] == 5:
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block3"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))
                elif self.map[x][y] == 6:
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block4"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2))) 
                elif self.map[x][y] == 7:
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block5"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2))) 
                elif self.map[x][y] == 9:
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["boundary"], #9 is to create boundary walls so that player doesn't cross over the game
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))

    # Check if the player is on a ladder or not
    def ladderCheck(self, laddersCollidedBelow,
                    wallsCollidedBelow, wallsCollidedAbove):
        if laddersCollidedBelow and len(wallsCollidedBelow) == 0:
            for ladder in laddersCollidedBelow:
                if ladder.getPosition()[1] >= self.Players[0].getPosition()[1]:
                    self.Players[0].onLadder = 1
                    self.Players[0].isJumping = 0
                    # Move the player down if he collides a wall above
                    if wallsCollidedAbove:
                        self.Players[0].updateY(3)
        else:
            self.Players[0].onLadder = 0

    # Check for coins collided and add the appropriate score
    def coinCheck(self, coinsCollected):
        for coin in coinsCollected:
            self.score += self.rewards["negative"]
            self.Players[0].setPosition((100, 290)) #player dies when reaches coin (coin is basically the enemy)
            # We also remove the coin entry from our map
            #self.map[int((coin.getPosition()[1] - 15 / 2) /
            #         15)][int((coin.getPosition()[0] - 15 / 2) / 15)] = 0
            self.lives += -1
            # Remove the coin entry from our list
            #self.Coins.remove(coin)
            # Update the coin group since we modified the coin list
            self.createGroups()

    # Check if the player wins
    def checkVictory(self):
        # If you touch the princess or reach the floor with the princess you
        # win!
        if self.Players[0].checkCollision(self.allyGroup) or self.Players[
                0].getPosition()[1] < 4 * 15:

            self.score += self.rewards["win"]

            # This is just the next level so we only clear the fireballs and
            # regenerate the coins
            self.Players[0].setPosition((100, 290))
            self.createGroups()

    # Redraws the entire game screen for us
    def redrawScreen(self, screen, width, height):
        screen.fill((40, 20, 0))  # Fill it with black
        # Draw all our groups on the background
        self.ladderGroup.draw(screen)
        self.playerGroup.draw(screen)
        self.coinGroup.draw(screen)
        self.wallGroup.draw(screen)
        self.allyGroup.draw(screen)

    # Update all the groups from their corresponding lists
    def createGroups(self):
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.ladderGroup = pygame.sprite.RenderPlain(self.Ladders)
        self.coinGroup = pygame.sprite.RenderPlain(self.Coins)
        self.allyGroup = pygame.sprite.RenderPlain(self.Allies)

    '''
    Initialize the game by making the map, generating walls, generating princess chamber, generating ladders randomly,
    generating broken ladders randomly, generating holes, generating coins randomly, adding the ladders and walls to our lists
    and finally updating the groups.
    '''

    def initializeGame(self):
        self.populateMap()
        self.createGroups()
