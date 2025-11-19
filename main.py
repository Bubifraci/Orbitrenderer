import numpy as np
import time
from models import planet
from models import bahn
from models import values
import renderer
from math import *

def solve_kepler(M, e, tol=1e-10, max_iter=100):
    E = M if e < 0.8 else np.pi

    for _ in range(max_iter):
        f  = E - e*np.sin(E) - M
        fp = 1 - e*np.cos(E)
        E_new = E - f/fp

        if abs(E_new - E) < tol:
            return E_new
        
        E = E_new

    raise RuntimeError("Newton iteration fehlgeschlagen")

def maneuver(pl, ba, dv):
    where = input("Wo soll das Manöver durchgeführt werden? (a für Apogäum, p für Perigäum)").lower()
    if(where != "a" or where != "p"):
        return maneuver(pl, ba, dv)
    if(dv == None):
        dvNew = input("Wie lautet das dv?")
        if(dvNew.isnumeric()):
            dv = float(dvNew)
        else:
            return maneuver(pl, ba, dv)
    
    vi = ba.getSpeedAtPoint(ba.ra)

    if(where == "p"):
        return None

def startSatellite(pl, ba, timeMultiplier = 50000, iterations = None):
    renderer.init()

    scale = 75000

    posX = None
    posY = None

    oldX = 0
    oldY = 0

    vals = values.Values()

    start = time.time()
    curTime = start
    repeat = True
    i = 0
    while (repeat):
        #Calculate  next step
        i += 1
        M = ba.calculateMeanAnomaly(curTime-start)
        E = solve_kepler(M, ba.e)
        pos = ba.getVector(E)
        posX = pos[0]
        posY = pos[1]

        distance = sqrt(pow(posX,2) + pow(posY,2)) - pl.radius*1000 #Planet ist im Zentrum

        velX = abs(posX-oldX)
        velY = abs(posY-oldY)

        #Es gibt zwei Möglichkeiten die momentane Geschindigkeit zu berechnen. 1 -> Über Tangenten in Bezug zur vorherigen Position. 2 -> Durch die Vis-Viva Gleichung.
        velocity = sqrt(pow(velX, 2) + pow(velY, 2))
        velocity1 = ba.getSpeedAtPoint(distance)

        print(f"X: {posX:.3f}; Y: {posY:.3f}; At time t={curTime-start:.2f}s; Distance from planet: {distance/1000:.3f}km; Velocity: tangential -> {velocity/1000:.3f}km/s or vis-viva -> {velocity1/1000:.3f}km/s")

        renderer.render(posX, posY, scale, pl.radius)

        curTime += 1 #Add a second
        if(iterations != None):
            if(i >= iterations):
                repeat = False
        time.sleep(1/timeMultiplier)
        oldX = posX
        oldY = posY

pl = planet.Planet("Erde", 6378, 5.972e24)
ba = bahn.Bahn(pl, 200, 600, 0, 0, 0)
startSatellite(pl, ba)