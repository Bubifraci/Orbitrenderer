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

    raise RuntimeError("Newton iteration did not converge.")

def startSatellite(timeFrame):
    renderer.init()
    pl = planet.Planet("Erde", 6378, 5.972e24)
    ba = bahn.Bahn(pl, 100, 100, 0, 0, 0)

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
        print(f"X: {posX}; Y: {posY}; At time t={curTime}")

        renderer.render(posX, posY)
        curTime += timeFrame
        time.sleep(timeFrame)

startSatellite(0.01)