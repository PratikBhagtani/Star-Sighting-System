from datetime import time, date, datetime
import math
import Navigation.prod.Angle as Angle
import os
from genericpath import isfile
import re
from operator import itemgetter, attrgetter
from xml.dom import minidom
from time import strftime, gmtime
from math import sqrt, pi, tan

class Fix:
    
    def __init__(self, logFile="logFile.txt"):
        try:
            if(isinstance(logFile, basestring) == False):
                raise ValueError
            if logFile == " ":
                raise ValueError
            myLogFile = open(logFile , 'a')
            myLogFile.write("LOG:\t" + strftime("%Y-%m-%d %H:%M:%S-06:00"))
            myLogFile.write("Start Of Log \n")
            myLogFile.close()
            self.sightingFileName = None
            self.logFile = logFile
            self.ariesFile = None
        except:
            raise ValueError("Fix.__init__:")
    def setSightingFile(self, sightingFile = None):
        if (not (isinstance(sightingFile, basestring))):
            raise ValueError("Fix.setSightingFile:  ")
        name,ext = os.path.splitext(sightingFile)
        if (ext != '.xml') or len(name) < 1:
            raise ValueError("Fix.setSightingFile:  ")
        Tfile = open(self.logFile, 'a')
        Tfile.flush()
        Tfile.write('LOG:\t' + strftime("%Y-%m-%d %H:%M:%S-06:00", gmtime()))
        Tfile.write(" Sighting file:\t"+os.path.abspath(sightingFile,gmtime()))
        # "Start of Log" + sightingFile)
        self.sightingFileName = sightingFile
        Tfile.close()
        
        return sightingFile
    
    
    def getSightings(self,assumedLatitude="0d0.0", assumedLongitude="0d0.0"):
        
        if(not(isinstance(assumedLatitude, basestring))):
            raise ValueError("Fix.getSightings:  Invalid assumeLatitude. Must be a string.")
        assumedLatitudeMatchObject = re.match(r'^([NS])?(-?[0-9]+)d([0-9]+(\.[0-9])?)$', assumedLatitude)
        if(assumedLatitudeMatchObject == None):
            raise ValueError("Fix.getSightings:  Invalid assumedLatitude form. Must be of form hxdy.y or (if h is missing) xdy.y.")
        h = "";
        xLatitudeValue = int(assumedLatitudeMatchObject.group(2))
        yLatitudeValue = float(assumedLatitudeMatchObject.group(3))
        if(assumedLatitudeMatchObject.group(1) == None):            
            if(xLatitudeValue != 0 or yLatitudeValue != 0.0):
                raise ValueError("Fix.getSightings:  Invalid assumedLatitude. Must be 0d0.0 if h is missing.")
        else:
            h = str(assumedLatitudeMatchObject.group(1))
        
        if(h != "" and h != "N" and h != "S"):
            raise ValueError("Fix.getSightings:  Invalid h. Must be 'N', 'S' or empty string")
        if(xLatitudeValue < 0 or xLatitudeValue >= 90):
            raise ValueError("Fix.getSightings:  Invalid x in assumedLatitude. Must be in range 0 <= x < 90")
        if(yLatitudeValue < 0.0 or yLatitudeValue >= 60.0):
            raise ValueError("Fix.getSightings:  Invalid y in assumedLatitude. Must be in range 0.0 <= y < 60.0")
        
        if(not(isinstance(assumedLongitude, basestring))):
            raise ValueError("Fix.getSightings:  Invalid assumedLongitude. Must be a string.")
        assumedLongitudeMatchObject = re.match(r'^(-?[0-9]+)d([0-9]+(\.[0-9])?)$', assumedLongitude)
        if(assumedLongitudeMatchObject == None):
            raise ValueError("Fix.getSightings:  Invalid assumedLongitude form. Must be of form xdy.y.")
        xLongitudeValue = int(assumedLongitudeMatchObject.group(1))
        yLongitudeValue = float(assumedLongitudeMatchObject.group(2))
        if(xLongitudeValue < 0 or xLongitudeValue >= 360):
            raise ValueError("Fix.getSightings:  Invalid x in assumedLongitude. Must be in range 0 <= x < 360")
        if(yLongitudeValue < 0.0 or yLongitudeValue >= 60.0):
            raise ValueError("Fix.getSightings:  Invalid y in assumedLongitude. Must be in range 0.0 <= y < 60.0")
          
        if(self.sightingFileName == None):
            raise ValueError("Fix.getSightings:  no sighting file has been set.")
        if(self.starFile == None):
            raise ValueError("Fix.getSightings:  Star file not set.")
        if(self.ariesFile == None):
            raise ValueError("Fix.getSightings:  Aries file not set.")
        doc = minidom.parse(self.sightingFileName)
        sightings = doc.getElementsByTagName("sighting")
        sightingList = []
        for index in sightings:           
            if index.getElementsByTagName("body"):
                try:
                    rbody = index.getElementsByTagName("body")[0].childNodes[0].data
                except IndexError:
                    print("Values Out Of Range:")
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
                try:
                    robserb = index.getElementsByTagName("observation")[0].childNodes[0].data
                    degreenminute = robserb.split("d")
                    degree = int(degreenminute[0])
                    minute = float(degreenminute[1])
                except IndexError:
                    print ("Fix.getSightings: IndexError. List Index out of Range")
            try:
                        
                if (degree < 0) or (degree > 90) or (minute < 0.0) or (minute > 60.0) :
                    raise ValueError("Fix.getSightings: Bad Data")
                else:
                    raise ValueError("Fix.getSightings: Bad Data")
            except:
                print ("Fix.getSightings:    ValueError")
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
            try:
                if index.getElementsByTagName("pressure"):
                    rpress = index.getElementsByTagName("pressure")[0].childNodes[0].data
                    if rpress != int(rpress):
                        raise ValueError
                    else:
                        rpress = int(rpress)
                else:
                    rpress = 1010
            except:
                print ("ValueError:")
            if index.getElementsByTagName("horizon"):
                rhorizon = index.getElementsByTagName("horizon")[0].childNodes[0].data
            else:
                rhorizon = "natural"
            ctemp = (rtemp - 32) / 9/5
            if rhorizon == "artificial":
                dip = 0.0
            else:
                dip = float(-0.97 * sqrt(float(rheight))) / 60.0
            meangle = Angle.Angle()
            robserb = meangle.setDegreesAndMinutes(robserb)
            refraction = ((-0.00452 * rpress)/(273 + ctemp)/math.tan(robserb))
            adjustedAltitute = robserb + dip + refraction
            adjustedAltitute = round(adjustedAltitute, 2)
            meangle.angle = adjustedAltitute
            sighting = [rbody, rdate, rtime, meangle.getString()]
            sightingList.append(sighting)
        sightingList = sorted(sightingList, key = itemgetter(1,2,3))

        
        currentISODate = date.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S%z")
        
        sum1 = 0
        sum2 = 0
                
        for sighting in sightingList:
            geographicPositionLatitude, geographicPositionLongitude = self.__calculateGeographicalPosition(self.starFile, sighting, self.ariesFile)
            if(geographicPositionLatitude != "" and geographicPositionLongitude != ""):
                adjustedDistance = self.__calculateAdjustedDistance(geographicPositionLatitude, geographicPositionLongitude, assumedLatitude, assumedLongitude, adjustedAltitute)
                azimuthAdjustment = self.__calculateAzimuthAdjustment(geographicPositionLatitude, assumedLatitude, adjustedDistance)
                sum1 = sum1 + (adjustedDistance * math.cos(azimuthAdjustment))
                sum2 = sum2 + (adjustedDistance * math.sin(azimuthAdjustment))
                angle = Angle.Angle()
                angle.setDegrees(azimuthAdjustment)
                myLogFile = open(self.logFile, "a+") 
                myLogFile.write("LOG: " + str(sighting.get_current_isodate()) + "-06:00 " + str(sighting.get_body()) + " " + str(sighting.get_the_date()) + " " + str(sighting.get_time()) + " " + sighting.get_angle_string() + " " + 
                                str(geographicPositionLatitude) + " " + str(geographicPositionLongitude) + " " + assumedLatitude + " " + assumedLongitude + " " + angle.getString() + " " + str(adjustedDistance) + "\n")
                myLogFile.close()
        
        
        assumedLatitude = assumedLatitude[1:]
        angle = Angle.Angle()
        angle.setDegreesAndMinutes(assumedLatitude)
        assumedLatitudeNumerical = angle.getDegrees()
        angle1 = Angle.Angle()
        angle1.setDegreesAndMinutes(assumedLongitude)
        assumedLongitudeNumerical = angle1.getDegrees()
        
        approximateLatitude = assumedLatitudeNumerical + (sum1 / 60)
        approximateLongitude = assumedLongitudeNumerical + (sum2 / 60)
        approximateLongitudeAngle = Angle.Angle()
        approximateLongitudeAngle.setDegrees(approximateLongitude)
        approximateLatitudeAngle = Angle.Angle()
        approximateLatitudeAngle.setDegrees(approximateLatitude)
                
        
        myLogFile = open(self.logFile, "a+")  
        myLogFile.write("LOG: " + currentISODate + "-06:00 Approximate latitude:    " + h + approximateLatitudeAngle.getString() + "    Approximate longitude:    " + approximateLongitudeAngle.getString() + "\n")  
        myLogFile.close()    
        
        return (approximateLatitude, approximateLongitude)

    

        
        
    def __calculateAdjustedDistance(self, geographicPositionLatitude, geographicPositionLongitude, assumedLatitude, assumedLongitude, adjustedAltitude):
        assumedLatitude = assumedLatitude[1:]
        assumedLatitudeAngle = Angle.Angle()
        assumedLatitudeAngle.setDegreesAndMinutes(assumedLatitude)
        
        assumedLatitudeNumerical = assumedLatitudeAngle.getDegrees()
        assumedLongitudeAngle = Angle.Angle()
        assumedLongitudeAngle.setDegreesAndMinutes(assumedLongitude)        
        assumedLongitudeNumerical = assumedLongitudeAngle.getDegrees()
        
        geographicPositionLongitudeAngle = Angle.Angle()
        geographicPositionLongitudeAngle.setDegreesAndMinutes(geographicPositionLongitude)        
        geographicPositionLongitudeNumerical = geographicPositionLongitudeAngle.getDegrees()
        
        geographicPositionLatitudeAngle = Angle.Angle()
        geographicPositionLatitudeAngle.setDegreesAndMinutes(geographicPositionLatitude)
        geographicPositionLatitdueNumerical = geographicPositionLatitudeAngle.getDegrees()
        
        LHA = geographicPositionLongitudeAngle.subtract(assumedLongitudeAngle)
        
        correctedAltitude = math.degrees(math.asin((math.sin(math.radians(geographicPositionLatitdueNumerical)) * math.sin(math.radians(assumedLatitudeNumerical)))
                                      + (math.cos(math.radians(geographicPositionLatitdueNumerical)) * math.cos(math.radians(assumedLatitudeNumerical)) * math.cos(math.radians(LHA)))))
        
        angle1 = Angle.Angle()
        angle1.setDegrees(adjustedAltitude)
        
        angle2 = Angle.Angle()
        angle2.setDegrees(correctedAltitude)
        
        
        adjustedDistance = angle1.subtract(angle2)
        return round(adjustedDistance, 2)
    
    def __calculateAzimuthAdjustment(self, geographicPositionLatitude, assumedLatitude, adjustedDistance):
        assumedLatitude = assumedLatitude[1:]
        angle = Angle.Angle()
        angle.setDegreesAndMinutes(assumedLatitude)
        assumedLatitudeNumerical = angle.getDegrees()
        angle2 = Angle.Angle()
        angle2.setDegreesAndMinutes(geographicPositionLatitude)
        geographicPositionLatitdueNumerical = angle2.getDegrees()
        azimuthAdjustment = math.acos((math.sin(math.radians(float(geographicPositionLatitdueNumerical))) - math.sin(math.radians(float(assumedLatitudeNumerical))) - math.sin(math.radians(float(adjustedDistance))))
                                      / math.cos(math.radians(float(assumedLatitudeNumerical))) * math.cos(math.radians(float(adjustedDistance))))
       
        return azimuthAdjustment
    
    def __calculateGeographicalPosition(self, starFileName, sighting, ariesFileName):
        declination = ""
        sideHourAngle = Angle.Angle()
        greenwichHourAngle1 = ""
        greenwichHourAngle2 = ""
        hours, minutes, seconds = sighting.get_time().split(':')
        with open(starFileName, "r") as f:
            for line in f:
                body, starDate, longitude, latitude = line.split()                
                if(body == sighting.get_body()):
                    declination = latitude
                    sideHourAngle.setDegreesAndMinutes(longitude)
                    break
                    
        with open(ariesFileName, "r") as f:
            foundGreenwichHourAngle = False
            for line in f:
                the_date, hour, angle = line.split()
                dateArray1 = str(the_date).split('/')
                dateArray2 = sighting.get_the_date().split('-')
                temp = dateArray2[0]
                dateArray2[0] = dateArray2[2]
                dateArray2[2] = temp[2:]
                temp2 = dateArray2[0]
                dateArray2[0] = dateArray2[1]
                dateArray2[1] = temp2
                dateObj1 = date.date(int(dateArray1[2]), int(dateArray1[0]), int(dateArray1[1]))
                dateObj2 = date.date(int(dateArray2[2]), int(dateArray2[0]), int(dateArray2[1]))
                
                if(foundGreenwichHourAngle == True):
                    greenwichHourAngle2 = angle
                    break                
                if(dateObj1 == dateObj2 and int(hours) == int(hour)):
                    greenwichHourAngle1 = angle
                    foundGreenwichHourAngle = True
        if(foundGreenwichHourAngle == True and declination != ""):
            
            s = (int(minutes) * 60) + int(seconds)
            angle1 = Angle.Angle()
            angle2 = Angle.Angle()
            angle1.setDegreesAndMinutes(greenwichHourAngle1)
            angle2.setDegreesAndMinutes(greenwichHourAngle2)
            degrees = abs(angle2.subtract(angle1))
            angle3 = Angle.Angle()
            angle3.setDegrees(degrees * (float(s)/3600))
            degrees2 = angle3.add(angle1)
            greenwichHourAngle = Angle.Angle()
            greenwichHourAngle.setDegrees(degrees2)
            
            degreesLongitude = greenwichHourAngle.add(sideHourAngle)
            greenwichHourAngleObservation = Angle.Angle()
            greenwichHourAngleObservation.setDegrees(degreesLongitude)
            return (declination, greenwichHourAngleObservation.getString())
            
        else:
            raise ValueError ("Fix.Pos(), Error")
            
        return ("", "")
            
            
    def __setSightingAttributes(self, sightings, index):
        height = 0
        temperature = 0
        pressure = 0 
        horizon = ""
        body = sightings[index].getElementsByTagName("body")[0].childNodes[0].data
        theDate = sightings[index].getElementsByTagName("date")[0].childNodes[0].data
        time = sightings[index].getElementsByTagName("time")[0].childNodes[0].data
        observation = sightings[index].getElementsByTagName("observation")[0].childNodes[0].data
        
        heightElements = sightings[index].getElementsByTagName("height")
        if(len(heightElements) == 0):
            height = 0.0
        else:
            height = heightElements[0].childNodes[0].data
            
        temperatureElements = sightings[index].getElementsByTagName("temperature")
        if(len(temperatureElements) == 0):
            temperature = 72
        else:
            temperature = temperatureElements[0].childNodes[0].data
            
        pressureElements = sightings[index].getElementsByTagName("pressure")
        if(len(pressureElements) == 0):
            pressure = 1010 
        else:
            pressure = pressureElements[0].childNodes[0].data 
                   
        horizonElements = sightings[index].getElementsByTagName("horizon")
        if(len(horizonElements) == 0):
            horizon = "Natural"
        else:
            horizon = horizonElements[0].childNodes[0].data
            
        return (height, temperature, pressure, horizon, body, theDate, time, observation)
        
        
    
    def setAriesFile(self,ariesFile):
        try:
            if not(ariesFile.find('.txt')>0):
                raise ValueError('Fix.setAriesFile:  ')
            temp = open(ariesFile,'r')
            writelog = open(self.logFile,'a')
            writelog.flush()
            writelog.write("\nLOG: " + strftime("%Y-%m-%d %H:%M:%S-06:00",))
            writelog.write(' Aries file:\t'+os.path.abspath(ariesFile))
            writelog.close()
            temp.close()
            self.ariesFile = ariesFile
            return os.path.abspath(ariesFile)
              
        except:
            raise ValueError('Fix.setAriesFile:  ')    
    def setStarFile(self,starFile):
        try:
            if not(starFile.find('.txt')>0):
                raise ValueError('Fix.setStarFile: ')
            temp = open(starFile,'r')
            writelog = open(self.logFile,'a')
            writelog.flush()
            writelog.write("\nLOG: " + strftime("%Y-%m-%d %H:%M:%S-06:00"))
            writelog.write(' Star file:\t'+os.path.abspath(starFile))
            writelog.close()
            temp.close()
            self.StarFile = starFile
            return os.path.abspath(starFile)
        except:
            raise ValueError('Fix.setStarFile: ')
        