import pygame
import sys

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

run = True

def render(posX, posY):
    screen.fill((0, 0, 0))
    satRen = pygame.draw.circle(posX, posY, 1.0, 1.0)
    pygame.display.update()
    pygame.time.delay(10)