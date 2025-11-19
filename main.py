import numpy as np
import time
from models import planet
from models import bahn
import renderer

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

def startSatellite(pl, ba, timeFrame = 0.01):
    renderer.init()

    timeMultiplier = 5000

    orbit_radius_px = 50 #Meter pro Pixel
    scale = ba.a/orbit_radius_px

    posX = None
    posY = None

    start = time.time()
    curTime = start
    while True:
        #Calculate  next step
        M = ba.calculateMeanAnomaly(curTime-start)
        E = solve_kepler(M, ba.e)
        pos = ba.getVector(E)
        posX = pos[0]
        posY = pos[1]
        print(f"X: {posX}; Y: {posY}; At time t={curTime-start}")

        renderer.render(posX, posY, scale, pl.radius)

        curTime += timeFrame * timeMultiplier
        time.sleep(timeFrame)

pl = planet.Planet("Erde", 6378, 5.972e24)
ba = bahn.Bahn(pl, 200, 6000, 0, 0, 0)
startSatellite(pl, ba, 0.01)