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
    where = input("Wo soll das Manöver durchgeführt werden? (a für Apogäum, p für Perigäum): ")
    if(where.lower() != "a" and where.lower() != "p"):
        return maneuver(pl, ba, dv)
    if(dv == None):
        dvNew = input("Wie lautet das dv (in m/s)?: ")
        if(dvNew.isnumeric()):
            dv = float(dvNew)
        else:
            return maneuver(pl, ba, dv)

    r = 0.0
    vals = values.Values()
    if(where == "p"):
        r = ba.rp
    else:
        r = ba.ra
    newV = ba.getSpeedAtPoint(r) + dv
    newA = 1.0/(-(pow(newV, 2)/(vals.G*pl.mass)) + 2.0/r)
    otherR = 2*newA-r

    newBahn = None
    if(where == "p"):
        newBahn = bahn.Bahn(pl, r/1000, otherR/1000, ba.inclination, ba.raan, ba.w, ba.anomaly, ba.tp)
    else:
        newBahn = bahn.Bahn(pl, otherR/1000, r/1000, ba.inclination, ba.raan, ba.w, ba.anomaly, ba.tp)
    startSatellite(pl, ba, ba2=newBahn)

def calculateCoordinates(pl, ba, title, curTime, start, oldX, oldY):
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

        print(f"{title}: X: {posX:.3f}; Y: {posY:.3f}; At time t={curTime-start:.2f}s; Distance from planet: {distance/1000:.3f}km; Velocity: tangential -> {velocity/1000:.3f}km/s or vis-viva -> {velocity1/1000:.3f}km/s")
        return[posX, posY]
    

def startSatellite(pl, ba, timeMultiplier = 50000, iterations = None, ba2 = None):
    renderer.init()

    scale = 75000

    oldX = 0
    oldY = 0
    oldX2 = 0
    oldY2 = 0

    vals = values.Values()

    start = time.time()
    curTime = start
    repeat = True
    i = 0
    while (repeat):
        i += 1
        posX, posY = calculateCoordinates(pl, ba, "Original", curTime, start, oldX, oldY)
        if(ba2 != None):
            posX2, posY2 = calculateCoordinates(pl, ba2, "New", curTime, start, oldX2, oldY2)
            renderer.render(posX, posY, scale, pl.radius, posX2, posY2)
            oldX2 = posX2
            oldY2 = posY2
        else:
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
maneuver(pl, ba, None)