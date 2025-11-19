import pygame
import sys

#Window Einstellungen
screen_width = 800
screen_height = 600

screen = None

#Farben Presets
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Mitte des Screens, wo der Planet liegen wird
centerX = screen_width/2
centerY = screen_height/2

#Initialisiere
def init():
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.init()

#Rendere ein/zwei Umlaufbahnen
def render(posX, posY, scale, plRadius, posX2 = None, posY2 = None):
    global screen
    screen.fill((0, 0, 0))

    #Koordinaten der ersten Umlaufbahn mit Skalierung
    x = int(centerX + posX / scale)
    y = int(centerY + posY / scale)

    #Zeichne
    pygame.draw.circle(screen, WHITE, (x, y), 4)

    #Berechnen der Koordinaten und einzeichnen der zweiten Umlaufbahn mit Skalierung
    if(posX2 != None and posY2 != None):
        x2 = int(centerX + posX2 / scale)
        y2 = int(centerY + posY2 / scale)
        pygame.draw.circle(screen, RED, (x2, y2), 4)

    #Einzeichnen des Planeten im Maßstab 1/1000
    pygame.draw.circle(screen, BLUE, (centerX, centerY), plRadius/1000)
    pygame.display.update()