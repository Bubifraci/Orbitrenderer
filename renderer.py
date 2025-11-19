import pygame
import sys

screen_width = 800
screen_height = 600

screen = None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

centerX = screen_width/2
centerY = screen_height/2

def init():
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.init()


def render(posX, posY, scale, plRadius, posX2 = None, posY2 = None):
    global screen
    screen.fill((0, 0, 0))

    x = int(centerX + posX / scale)
    y = int(centerY + posY / scale)

    pygame.draw.circle(screen, WHITE, (x, y), 4)
    if(posX2 != None and posY2 != None):
        x2 = int(centerX + posX2 / scale)
        y2 = int(centerY + posY2 / scale)
        pygame.draw.circle(screen, RED, (x2, y2), 4)

    pygame.draw.circle(screen, BLUE, (centerX, centerY), plRadius/1000)
    pygame.display.update()