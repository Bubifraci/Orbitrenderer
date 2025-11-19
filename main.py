import numpy as np
import time
from models import planet
from models import bahn
from models import values
import renderer
from math import *

#Helfer-Methode um zu prüfen, ob ein Wert als float geparsed werden kann
def isFloat(val):
    try:
        a = float(val)
        return True
    except ValueError:
        return False

#Lösen der Kepler-Gleichung durch Newton-Verfahren. M ist die mittlere Anomalie, e ist die Exzentrizität, tol ist die Fehlertoleranz und max_iter begrenzt die Anzahl der Iterationen
def solve_kepler(M, e, tol=1e-10, max_iter=100):
    #Erstbeste Schätzung auf Basis der Exzentrizität
    E = M if e < 0.8 else np.pi

    #Iteriere, bis die Grenze erreicht wird (bzw. das Ergebnis innerhalb der Fehlertoleranz liegt)
    for _ in range(max_iter):
        #Stelle die Keplergleichung um, sodass der Term und M auf einer SEite liegt
        f  = E - e*np.sin(E) - M
        #Leite ab
        fp = 1 - e*np.cos(E)
        #Rekursived Newton-Verfahren
        E_new = E - f/fp

        #Liegt innerhalb der Fehlergrenze? Gebe das Ergebnis zurück!
        if abs(E_new - E) < tol:
            return E_new
        
        #Ansonsten wiederhole
        E = E_new

    raise RuntimeError("Newton iteration fehlgeschlagen")

#Dialogsystem zum Ausführen eines Manövers nach 2.2b. Rendert die originale Bahn (in weiß) und die neue Bahn nach dem Manöver (in rot)
def maneuver(pl, ba, dv, timeMultiplier = 50000):
    where = input("Wo soll das Manöver durchgeführt werden? (a für Apogäum, p für Perigäum): ")
    if(where.lower() != "a" and where.lower() != "p"):
        return maneuver(pl, ba, dv)
    if(dv == None):
        dvNew = input("Wie lautet das dv (in m/s)?: ")
        if(isFloat(dvNew)):
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
    #Durch Umstellen der vis-viva Gleichung lässt sich die große Halbachse a durch Kenntnis der Geschwindigkeit am Apogäum/Perigäum bestimmen
    newA = 1.0/(-(pow(newV, 2)/(vals.G*pl.mass)) + 2.0/r)
    #Der Radius des Perigäums/Apogäums lässt sich durch die Definition von a = 0.5(ra+rb) berechnen
    otherR = 2*newA-r

    #Initialisiere neue Bahn als Objekt und starte das Rendern beider Umlaufbahnen (original und neu)
    newBahn = None
    if(where == "p"):
        newBahn = bahn.Bahn(pl, r/1000 - pl.radius, otherR/1000 - pl.radius, ba.inclination, ba.raan, ba.w, ba.anomaly, ba.tp)
    else:
        newBahn = bahn.Bahn(pl, otherR/1000 - pl.radius, r/1000 - pl.radius, ba.inclination, ba.raan, ba.w, ba.anomaly, ba.tp)
    startSatellite(pl, ba, ba2=newBahn, timeMultiplier=timeMultiplier)

#Logik um Koordinaten zu berechnen
def calculateCoordinates(pl, ba, title, curTime, start, oldX, oldY):
        #Berechne mittlere Anomalie M, damit per Kepler-Gleichung die exzentrische Anomalie E, um dann die Position zu berechnen
        M = ba.calculateMeanAnomaly(curTime-start)
        E = solve_kepler(M, ba.e)
        pos = ba.getVector(E)
        posX = pos[0]
        posY = pos[1]

        #Berechne die Distanz vom Planetenzentrum (0, 0) mittels Norm des Vektors
        distance = sqrt(pow(posX,2) + pow(posY,2)) - pl.radius*1000

        #Es gibt zwei Möglichkeiten die momentane Geschindigkeit zu berechnen. 1 -> Über Tangenten in Bezug zur vorherigen Position. 2 -> Durch die Vis-Viva Gleichung.
        velX = abs(posX-oldX)
        velY = abs(posY-oldY)

        velocity = sqrt(pow(velX, 2) + pow(velY, 2))
        velocity1 = ba.getSpeedAtPoint(sqrt(pow(posX, 2) + pow(posY, 2)))

        print(f"{title}: X: {posX:.3f}; Y: {posY:.3f}; Zur Zeit t={curTime-start:.2f}s; Distanz vom Planeten: {distance/1000:.3f}km; Geschwindigkeit: Tangential -> {velocity/1000:.3f}km/s oder vis-viva -> {velocity1/1000:.3f}km/s")
        return[posX, posY]
    
#Funktion zum Starten eines Satelliten, ggf. auch mit einer zweiten Umlaufbahn, falls ein Manöver ausgeführt wurde
def startSatellite(pl, ba, timeMultiplier = 50000, iterations = None, ba2 = None):
    #Initialisierung des Renderers mit PyGame
    renderer.init()

    #Skalierung der Distanzen, da sie sonst nicht alle in einem Display passen würden
    scale = 75000

    #Daten der vorherigen Berechnung, um Geschwindigkeit per Tangente zu berechnen
    oldX = 0
    oldY = 0
    oldX2 = 0
    oldY2 = 0

    #Initialisierung von Konstanten
    vals = values.Values()

    #Zeiteinstellungen, um korrekte Zeitschritte durchzuführen
    start = time.time()
    curTime = start

    #Logik für Iterationen. Solange repeat true ist, rendert das Program. Nützlich falls bspw. nur 10 Iterationen durchgeführt werden sollen (eher für Testzwecke)
    repeat = True
    i = 0
    while (repeat):
        i += 1

        #Berechne Koordinaten der originalen Umlaufbahn
        posX, posY = calculateCoordinates(pl, ba, "Original", curTime, start, oldX, oldY)

        #Falls Manöver durchgeführt wurde, berechne Koordinaten der aktuellen/neuen Umlaufbahn
        if(ba2 != None):
            posX2, posY2 = calculateCoordinates(pl, ba2, "New", curTime, start, oldX2, oldY2)

            #Render die Satelliten
            renderer.render(posX, posY, scale, pl.radius, posX2, posY2)

            #Setzen der ehemaligen Werte für Tangenten
            oldX2 = posX2
            oldY2 = posY2
        else:
            #Render die Satelliten
            renderer.render(posX, posY, scale, pl.radius)
        

        curTime += 1 #Sekunde fortschreiten

        #Iterationslogik
        if(iterations != None):
            if(i >= iterations):
                repeat = False

        #Skalierung der Zeit! Standardweise auf 50.000 gesetzt, d.h. pro realer Sekunde vergehen 50.000 Sekunden in der Simulation
        time.sleep(1/timeMultiplier)

        #Setzen der ehemaligen Daten
        oldX = posX
        oldY = posY

#Diese Funktion fungiert als simples Dialogsystem, um alle relevanten Daten vom Nutzer zu erfragen
def startProgram():
    pl = None

    title = None
    mass = None
    radius = None

    print("Willkommen zum Umlaufbahnrenderer! Zunächst, wir fangen damit an, den Planeten einzurichten, um den die Objekte rotieren.")

    #Planeten-Setup
    plName = input("Namen des Planeten (wird Erde eingegeben, werden sofort die Werte für die Erde initialisiert): ")
    if(plName.lower() == "erde"):
        pl = planet.Planet("Erde", 6378, 5.972e24)
        title = "Erde"
        mass = pl.mass
        radius = 6378
    else:
        title = plName
        plMass = ""
        while(not isFloat(plMass)):
            plMass = input(f"Gebe nun die Masse des Planeten {title} an (in kg): ")
        mass = float(plMass)
        plRadius = ""
        while(not isFloat(plRadius)):
            plRadius = input(f"Gebe nun den Radius des Planeten {title} an (in km): ")
        radius = float(plRadius)
    shallContinue = ""
    while(shallContinue.lower() != "j" and shallContinue.lower() != "n"):
        shallContinue = input(f"Der Planet {title} hat die Masse {mass}kg und den Radius {radius}km. Ist das korrekt (j/n)? ")
    if(shallContinue == "n"):
        return startProgram()
    pl = planet.Planet(title, radius, mass)

    #Umlaufbahn Setup
    print("\nNun kümmern wir uns um die Umlaufbahn. ")
    baRp = ""
    while(not isFloat(baRp)):
        baRp = input("Gebe die Höhe am Perigäum der Umlaufbahn an: ")
    rp = float(baRp)
    baRa = ""
    while(not isFloat(baRa)):
        baRa = input("Gebe die Höhe am Apogäum der Umlaufbahn an: ")
    ra = float(baRa)
    ba = bahn.Bahn(pl, rp, ra, 0, 0, 0)

    #Zeitskalierung
    timeScale = input("Wie soll die Zeit modifiziert werden (wieviele Sekunden in der Simulation pro echter Sekunde) -> Standardmäßig auf 50.000: ")
    if(isFloat(timeScale)):
        timeScale = float(timeScale)
    else:
        timeScale = 50000

    #Manöver ausführen? (Aufgabe 2.2b)
    shallManeuver = ""
    while(shallManeuver.lower() != "j" and shallManeuver.lower() != "n"):
        shallManeuver = input("Soll ein Manöver durchgeführt werden? (j/n) ")
    if(shallManeuver == "j"):
        maneuver(pl, ba, None, timeMultiplier=timeScale)
    else:
        startSatellite(pl, ba, timeMultiplier=timeScale)

startProgram()