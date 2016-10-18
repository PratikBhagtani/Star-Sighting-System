'''
Created on Oct 11, 2016

@author: pRaTiK BhAgTaNi
'''
from datetime import time, date
import math
from Navigation.prod.Angle import Angle as AI
import os
import xml.dom.minidom
from time import strftime
from math import sqrt
class Fix:
    
    def __init__(self, logFile="logFile.txt"):
        if(isinstance(logFile, basestring) == False):
            raise ValueError
        fileo = open(logFile , 'a')
        fileo.write("LOG:\t" + strftime("%Y-%m-%d %H:%M:%S-06:00"))
        fileo.write("Start Of Log. \n")
        fileo.close()
        self.logFile = logFile
    
    
    def setSightingFile(self, sightingFile = None):
        if (not (isinstance(sightingFile, str))):
            raise ValueError("Fix.setSightingFile:  ")
        name,ext = os.path.splitext(sightingFile)
        if (ext != '.xml') or len(name) < 1:
            raise ValueError("Fix.setSightingFile:  ")
        Tfile = open(self.logFile, 'a')
        Tfile.flush()
        Tfile.write('LOG:\t' + strftime("%Y-%m-%d %H:%M:%S-06:00") + ':\tStart of sighting file ' + sightingFile+'\n') # "Start of Log" + sightingFile)
        self.newsightFile = sightingFile
        Tfile.close()
        
        return sightingFile
    
    
    def getSightings(self):
        
        approximateLatitude = "0d0.0"
        approximateLongitude = "0d0.0"
        

        TEfile = xml.dom.minidom.parse(self.newsightFile)
        rxml = TEfile.documentElement
        rsightings = rxml.getElementsByTagName("sighting")
        for index in rsightings:           
            if index.getElementsByTagName("body"):
                rbody = index.getElementsByTagName("body")[0].chileNodes[0].data
            else:
                raise ValueError("Fix.getSightings: Bad Data")
            if index.getElementsByTagName("time"):
                rtime = index.getElementsByTagName("time")[0].childNodes[0].data
            else:
                raise ValueError("Fix.getSightings: Bad Data")
            if index.getElementsByTagName("date"):
                rdate = index.getElementsByTagName("date")[0].childNodes[0].data
            else:
                raise ValueError("Fix.getSightings: Bad Data")
            if index.getElementsByTagName("observation"):
                robserb = index.getElementsByTagName("observation")[0].childNodes[0].data
                degreenminute = robserb.split("d")
                degree = int(degreenminute[0])
                minute = float(degreenminute[1])
                if (degree < 0) or (degree > 90) or (minute < 0.0) or (minute > 60.0) :
                    raise ValueError("Fix.getSightings: Bad Data")
            else:
                raise ValueError("Fix.getSightings: Bad Data")
            if index.getElementsByTagName("height"):
                rheight = index.getElementsByTagName("height")[0].childNodes[0].data
            else:
                rheight = 0
            if index.getElementsByTagName("temperature"):
                rtemp = index.getElementsByTagName("temperature")[0].childNodes[0].data
                rtemp = int(rtemp)
                if rtemp < -20 and rtemp > 120:
                    raise ValueError
            else:
                rtemp = 72
                rtemp = int(rtemp)
            if index.getElementsByTagName("pressure"):
                rpress = index.getElementsByTagName("pressure")[0].childNodes[0].data
                rpress = int(rpress)
            else:
                rpress = 1010
            if index.getElementsByTagName("horizon"):
                rhorizon = index.getElementsByTagName("horizon")[0].childNodes[0].data
            else:
                rhorizon = "natural"
            ctemp = (rtemp - 32) / 9/5
            if rhorizon == "artificial":
                dip = 0.0
            else:
                dip = float(-0.97 * sqrt(float(rheight))) / 60.0
            robserb = AI.setDegreesAndMinutes(self, robserb)
            refraction = ((-0.00452 * rpress)/(273 + ctemp)/math.tan(robserb))
            adjustedAltitute = robserb + dip + refraction
            adjustedAltitute = round(adjustedAltitute, 2)
            writelog = open("logFile.txt", 'a')
            writelog.flush()
            writelog.write('LOG: \t' + strftime("%Y-%m-%d %H:%M:%S-06:00") + "\t" + rbody + "\t" + rdate + "\t" + rtime + "\t" + adjustedAltitute + "\n")
        writelog.write('LOG: \t' + strftime("%Y-%m-%d %H:%M:%S-06:00") + "\t End of sighting file " + self.newsightFile)
        writelog.close()        
        return (approximateLatitude, approximateLongitude)