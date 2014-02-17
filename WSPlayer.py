
# File: WSPlayer.py

# Name: Will Hawkins

# Date: January 10th, 2013

# This programe creates instances of each player for the World Series simulation

# and stores all of their pertinent information.


from random import *

class WSPlayer:

    # Initializes all instance vars for WSPlayer class. 
    def __init__(self, fName, lName, batAve, hits, doubs, trips, homers, numSims, team):
        self.fName = fName
        self.lName = lName
        self.batAve = batAve
        self.totalHits = hits
        self.singAve = (hits - doubs - trips - homers) / hits
        self.doubAve = doubs / hits
        self.tripAve = trips / hits
        self.countHits = False
        self.base = -1
        if team == 'g':
            self.team = "Giants"
        else:
            self.team = "Tigers"

    # Adds stat-counting variables needed for play-by-play.
    def initializeCounters(self):
        self.countHits = True
        self.rbisCount = 0
        self.runsCount = 0
        self.doubCount = 0
        self.tripCount = 0
        self.homeCount = 0


    # Returns the number of bases the player advances (0 if out).
    def batting(self):
        if self.hit():
            res = self.processHit()
        else:
            return 0
        poss = ["o", "s", "d", "t", "h"]
        return poss.index(res)

            
    # Returns a boolean if the player gets a hit.
    def hit(self):
        genSwing = random()
        if genSwing < self.batAve:
            return True
        return False


    # Determines if player's hit is single, double, trip, homer.
    def processHit(self):
        hit = random()
        if hit < self.singAve:
            return "s"
        elif hit < self.singAve + self.doubAve:
            return "d"
        elif hit < self.singAve + self.doubAve + self.tripAve:
            return "t"
        else:
            return "h"

    def getName(self):
        return self.fName + " " + self.lName

    def getLName(self):
        return self.lName

    def getFName(self):
        return self.fName

    def getAbbName(self):
        return self.fName[0] + ". " + self.lName

    def setBase(self, baseNum):
        self.base = baseNum

    def getBase(self):
        return self.base

    def getTeam(self):
        return self.team

    # Updates batting statistics.
    # Stat values: RBI=0, RUNS=1, DOUB=2, TRIP=3, HOME=4.
    def setStat(self, value, stat):
        if stat == 0:
            self.rbisCount += value
        elif stat == 1:
            self.runsCount += value
        elif stat == 2:
            self.doubCount += value
        elif stat == 3:
            self.tripCount += value
        elif stat == 4:
            self.homeCount += value

    def getStat(self, stat):
        if stat == 0:
            return self.rbisCount
        elif stat == 1:
            return self.runsCount
        elif stat == 2:
            return self.doubCount
        elif stat == 3:
            return self.tripCount
        elif stat == 4:
            return self.homeCount
        

