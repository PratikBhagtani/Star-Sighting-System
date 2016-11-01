from datetime import time, date
import math
import Navigation.prod.Angle as Angle
import os
import xml.dom.minidom
from time import strftime, gmtime
from math import sqrt, pi, tan
from cgi import logfile
from operator import itemgetter
class Fix:
    
    def __init__(self, logFile="logFile.txt"):
        try:
            if(isinstance(logFile, basestring) == False):
                raise ValueError
            if logFile == " ":
                raise ValueError
            fileo = open(logFile , 'a')
            fileo.write("LOG:\t" + strftime("%Y-%m-%d %H:%M:%S-06:00"))
            fileo.write("Start Of Log \n")
            fileo.close()
            self.sightingFile = None
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
        self.sightingFile = sightingFile
        Tfile.close()
        
        return sightingFile
    
    
    def getSightings(self):
        
        approximateLatitude = "0d0.0"
        approximateLongitude = "0d0.0"
    

        TEfile = xml.dom.minidom.parse(self.sightingFile)
        rxml = TEfile.documentElement
        rsightings = rxml.getElementsByTagName("sighting")
        for index in rsightings:           
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
            singleSight = [rbody, rdate, rtime, meangle.getString()]
            col = []
            col.append(singleSight)
        col = sorted(col, key = itemgetter(1,2,3))
        writelog = open(self.logFile,'a')
        for i in col:
            (lat,long) = self.pos(str(i[0]),str(i[1]),str(i[2]))
            writelog.write("\nLOG:\t" + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime()))
            writelog.write(":\t"+ i[0] + ":\t"+ i[1] + ":\t"+ i[2] + ":\t"+ i[3]+ ":\t"+ str(lat.getString()))
        writelog.write("\nLOG:\t" + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime()))
        writelog.write(':\nEnd of sighting file '+self.sightingFile)
        writelog.flush()
        writelog.close()
        return (approximateLatitude, approximateLongitude)
    
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
       
    def pos(self, body=None, observationDate = None, observationTime = None):
        
        if(observationTime == None):
            raise ValueError('Fix.getGeographicPosition: hour missing')
        if(body==None):
            raise ValueError('Fix.getGeographicPosition: body missing')
        if(observationDate==None):
            raise ValueError('File.getPositions: date missing')
        writefile = open('starFile.txt','a') 
        starFile = self.starFile
        ariesFile = self.ariesFile
        tempArr = str(observationTime).split(':')
        observationHour = int(tempArr[0])
        s = (int(tempArr[1])*60) +int(tempArr[2])
        PosLat = Angle.Angle()
        PosLong = Angle.Angle()
        ghaAries1 = ''
        ghaAries2 = ''
        tempArray = observationDate.split('-')
        previousStarObservation = None
        shaStar = None
        observationYear = int(tempArray[0])%2000
        observationMonth = int(tempArray[1])
        observationDay = int(tempArray[2])
        writefile = open('starFile.txt','a')
        writefile2 = open(starFile,'r')
        starObservations = writefile2.readlines()
        for Observation in starObservations:
            temp = Observation.split('\t')
                
            bodyInStarFile = temp[0]
                
            if(body==bodyInStarFile):
                    
                date = temp[1].split('/')

                if(observationYear <= int(date[2]) and observationMonth <= int(date[0]) and observationDay <= int(date[1]) ):
                    previousStarObservation = temp
        PosLat.setDegreesAndMinutes(previousStarObservation[3])
        shaStar = previousStarObservation[2]
        shaStarAngle = Angle.Angle()
        shaStarAngle.setDegreesAndMinutes(shaStar)
        writefile1 = open(ariesFile,'r')
        ariesObservations = writefile1.readlines()    
        for Observation in ariesObservations:
            temp = Observation.split('\t')
            tempDate = str(observationMonth).zfill(2)+'/'+str(observationDay).zfill(2)+'/'+str(observationYear)
            if(tempDate == temp[0]):
                if(observationHour==23):
                    if(int(temp[1])==0):
                        ghaAries2 = temp[2]
                        writefile.write("\n gha2:"+ghaAries2)        
                if( observationHour == int(temp[1])):
                    ghaAries1 = temp[2]
                    writefile.write("\n gha1:"+ghaAries1)
                if(observationHour + 1 == int(temp[1])):
                    ghaAries2 = temp[2]
                    writefile.write("\n gha2:"+ghaAries2)    
        ghaAriesAngle1 = Angle.Angle()
        writefile.write('\n gha:'+str(ghaAries1))
        ghaAriesAngle1.setDegreesAndMinutes(ghaAries1)
        temp1 = float(ghaAriesAngle1.angle)
        ghaAriesAngle2 = Angle.Angle()
        ghaAriesAngle2.setDegreesAndMinutes(ghaAries2)
        temp2 = float(ghaAriesAngle2.angle)
        ghaAriesAngle = Angle.Angle()
        tempAngle = abs(temp2-temp1)
        tempAngle = float(tempAngle)*s/3600 
        ghaAriesAngle.setDegrees(tempAngle) 
        ghaAriesAngle.add(ghaAriesAngle1)
        PosLong.setDegrees(round(float(ghaAriesAngle.add(shaStarAngle)) % 360,1))               
        return (PosLat,PosLong)