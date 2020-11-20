import pygame

HEIGHT = 600
WIDTH = 800
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


class SpaceShip(pygame.Rect):

    def __init__(self, color=GREEN, width=40, height=20, speed=3):
        self.x = 400
        self.y = 550
        self.color = color
        self.width = width
        self.height = height
        self.speed = 7
        self.health = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def moveRight(self):
        if self.x + self.width <= WIDTH - 5:
            self.x += self.speed
    
    def moveLeft(self):
        if self.x >= 5:
            self.x -= self.speed



class Shelter(pygame.Rect):

    def __init__(self, x, y, width, height, color=GREEN):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.parts = []
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
    

class Lazer(pygame.Rect):
    
    def __init__(self, x, y, width=3, height=10, color=(0,255,0), speed=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.kd = 0

    def update(self):
        self.y -= self.speed

    def draw(self, win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height))


class Enemy(pygame.Rect):
    
    y_direction = 0
    direction = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 25
        self.width = 25

    def draw(self, win):
        pygame.draw.rect(win, WHITE, pygame.Rect(self.x, self.y-self.y_direction, self.width, self.height))