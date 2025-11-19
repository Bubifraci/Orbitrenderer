from math import *
from models import values

class Bahn():
    def __init__(self, pl, rp, ra, inclination, raan, w, anomaly = None, tp=0):
        vals = values.Values()
        self.pl = pl
        self.rp = (rp + pl.radius) * 1000
        self.ra = (ra + pl.radius) * 1000
        self.a = 0.5*(ra+rp)
        c = self.a - rp
        self.e = c/self.a
        self.inclination = inclination
        self.raan = raan
        self.w = w
        self.anomaly = anomaly
        self.T = 2*pi*sqrt(pow(self.a, 3)/(vals.G*pl.mass))
        self.anomaly = None
        self.tp = tp

    def setAnomaly(self, anomalyE):
        anomaly = 2*atan(tan(anomalyE/2)/sqrt((1-self.e)/(1+self.e)))
        return anomaly

    def getSpeedAtPoint(self, r):
        vals = values.Values()
        v = sqrt(vals.G*self.pl.mass*((2/r)-(1/self.a)))
        return v
    
    def getVector(self, eAnomaly):
        x = self.a*(cos(eAnomaly)-self.e)
        y = self.a*sqrt(1-pow(self.e, 2))*sin(eAnomaly)
        return [x, y]
    
    def calculateMeanAnomaly(self, time):
        return (2*pi)/self.T*(time-self.tp)
