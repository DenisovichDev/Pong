# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 16:29:00 2020

Authors: Bhaswar Chakraborty and Anusha Tripathi
"""
import pygame
import random
import math
import sys
#import pandas as pd
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()


# Variables

HEIGHT = 600
WIDTH = 1080
BORDER = 20
VELOCITY = 1
initFR = 330
speedFactor = 40
FRAMERATE = initFR
fgColor = pygame.Color(125, 125, 125)
bgColor = pygame.Color(255, 255, 255)
invisible = bgColor  # pygame.Color("blue")
ballColor = pygame.Color(200, 10, 0)
wall = pygame.Color(10, 155, 100)
clock = pygame.time.Clock()

# define the classes


class Paddle:
    """
    The Paddle Class
    """
    HEIGHT = 120
    WIDTH = 20

    def __init__(self, y):
        self.y = y

    def show(self, colour):
        global screen, fgColor

        pygame.draw.rect(screen, colour, pygame.Rect(WIDTH-self.WIDTH, self.y-self.HEIGHT//2, self.WIDTH, self.HEIGHT))

    def update(self):
        global fgColor,bgColor
        newy = pygame.mouse.get_pos()[1]
        if newy-self.HEIGHT//2 > BORDER\
            and newy+self.HEIGHT//2 < HEIGHT-BORDER:

            self.show(bgColor)
            self.y = newy
            self.show(fgColor)


class Ball:
    """
    The Ball Class
    """

    RADIUS = 20

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def show(self, colour):
        global screen
        pygame.draw.circle(screen, colour, (self.x, self.y), self.RADIUS)

    def update(self):

        global bgColor, ballColor, FRAMERATE, stop, speedFactor

        newx = self.x+self.vx
        newy = self.y+self.vy

        if newx < BORDER+self.RADIUS:
            self.vx = -self.vx
            collision()

        elif newy < BORDER+self.RADIUS or newy > HEIGHT-BORDER-self.RADIUS:
            self.vy = -self.vy
            collision()

        elif newx > WIDTH-Paddle.WIDTH-self.RADIUS and \
           ((player.y - Paddle.HEIGHT // 2 - self.RADIUS < newy < player.y + Paddle.HEIGHT // 2 + self.RADIUS)\
            or (distance((self.x, self.y), (WIDTH-Paddle.WIDTH, player.y-Paddle.HEIGHT//2)) <= self.RADIUS) or (distance((self.x,self.y),(WIDTH-Paddle.WIDTH, player.y+Paddle.HEIGHT//2))<=self.RADIUS)):
               self.vy = -self.vy
               FRAMERATE += speedFactor
               collision()

        elif newx == WIDTH-BORDER-self.RADIUS and \
            (player.y + (player.HEIGHT // 2) >= newy >= player.y - (player.HEIGHT // 2)):
                self.vx = -self.vx
                FRAMERATE += speedFactor
                collision()

                if not(player.y + (player.HEIGHT * (2 / 6)) > newy > player.y - (player.HEIGHT * (2 / 6))):
                    self.vy = -self.vy
                    collision()
                    FRAMERATE += speedFactor
        elif newx > WIDTH + self.RADIUS:
            self.vx, self.vy = 0, 0
            return 1
        else:
            self.show(invisible)
            self.x = self.x+self.vx
            self.y = self.y+self.vy
            self.show(ballColor)

# Functions


def game_over():
    global screen, v1, v2, FRAMERATE
    mixer.music.fadeout(1000)
    pygame.font.get_fonts()
    font = pygame.font.SysFont('comicsansms', 100)
    text = font.render('Game Over', True, pygame.Color('red'))
    textRect = text.get_rect()
    textRect.center = (WIDTH//2, HEIGHT//2)
    screen.blit(text, textRect)
    lose.play()
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                FRAMERATE = initFR
                mixer.music.play(-1)
                v1 = -1
                v2 = -1
                game_loop()
        pygame.display.update()



def collision():
    global stop
    if stop != 1:
        sound_col.play()


def distance(a, b):
    d = math.sqrt(math.pow((a[0]-b[0]), 2)+math.pow((a[1]-b[1]), 2))
    return d


# Initiating modules

# Generating Random numbers:
#random.randint(BORDER+Paddle.HEIGHT//2,HEIGHT-2*(BORDER+Paddle.HEIGHT//2))
#v2 = random.randint(-1,0)

# if v2==0:
#     v2=1
initPos = HEIGHT//2
v1 = -1
v2 = -1

# create player object
player = Paddle(initPos)


# Sound
mixer.music.load('Moneyforschool.mp3')
mixer.music.set_volume(0.18)
mixer.music.play(-1)
sound_col = mixer.Sound('hit.wav')
sound_col2 = mixer.Sound('beep.wav')
lose = mixer.Sound('Lost.wav')

# =================== Machine Learning ======================= #
#sample = open("game1.csv", "w")
#print("x,y,vx,vy,FR,Paddle.y", file=sample)

# pong = pd.read_csv("game1.csv")
# pong = pong.drop_duplicates()
#
# x = pong.drop(columns="Paddle.y")
# y = pong["Paddle.y"]
#
# from sklearn.neighbors import KNeighborsRegressor
# clf = KNeighborsRegressor(n_neighbors=3)
# clf.fit(x,y)
#
# df = pd.DataFrame(columns=['x','y','vx','vy','FR'])
# ============================================================= #

stop = 0
replay = 0
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        break


def game_loop():
    global screen, bgColor, fgColor, wall, HEIGHT, WIDTH, BORDER, stop, replay, ballColor, v1, v2

    ballplay = Ball(WIDTH - Ball.RADIUS - Paddle.WIDTH, player.y, v1 * VELOCITY, v2 * VELOCITY)


    running = True

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Squash Pong")
    pygame.draw.rect(screen, bgColor, pygame.Rect(0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, wall, pygame.Rect(0, 0, WIDTH, BORDER))
    pygame.draw.rect(screen, wall, pygame.Rect(0, 0, BORDER, HEIGHT))
    pygame.draw.rect(screen, wall, pygame.Rect(0, HEIGHT - BORDER, WIDTH, BORDER))
    ballplay.show(ballColor)
    player.show(fgColor)

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # toPredict = df.append({'x': ballplay.x, 'y': ballplay.y, 'vx': ballplay.vx, 'vy': ballplay.vy,'FR': FRAMERATE}, ignore_index=True)
        # shouldMove = clf.predict(toPredict)

        pygame.display.update()
        clock.tick(FRAMERATE)

        stop = ballplay.update()
        player.update()  # Type shouldMove

        if stop == 1:
            game_over()

        #print("{},{},{},{},{},{}".format(ballplay.x, ballplay.y, ballplay.vx, ballplay.vy, FRAMERATE, player.y), file=sample)


game_loop()
