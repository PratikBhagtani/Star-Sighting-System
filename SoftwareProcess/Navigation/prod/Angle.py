from string import strip
from idlelib.configDialog import is_int
from lib2to3.fixer_util import String
class Angle():
    
    def __init__(self):
        #self.angle = ...       set to 0 degrees 0 minutes
        self.ang = '0d0'
        return self.ang
        
        pass
    
    def setDegrees(self, degrees):
        if degrees == None:
       
            degrees = 0.0
            return degrees
       
        else:
            try:

                #degrees = input("Enter your data:" )
                degrees = degrees % 360
                
                return degrees
        
            except ValueError as v:
                print v
        
        pass
    
    def setDegreesAndMinutes(self,angleString):
        
        
        try:
            degree,minute = angleString.split("d")
            
            
            if minute > 0:
                degree = int(degree) 
                minute = float(minute) 
                minute = round(minute,1)
                angleString = degree+'d'+minute
                pass
            else:
                print "fail"
            return angleString
            
        except ValueError as b:
            print (b), '"Enter Degree in integer Value and Minutes in Integer or Float values."'
            
      
        pass
    
    def add(self, angle):
        
        try:
            degree,minute = angle.split("d")
            
            
            if minute > 0:
                degree = int(degree)
                degree = degree % 360 
                minute = float(minute) 
                minute = round(minute,1)
                angle = degree+'d'+minute
                self.Angle = Angle + angle
                degree,minute = self.Angle.split("d")
                degree = degree % 360
                if minute == 30:
                    self.Angle = degree + 0.5
                elif minute == 60:
                    self.Angle = degree + 1
                else:
                    self.Angle = degree
                return self.Angle
            
            
            else:
                print "fail"
            
        except ValueError as b:
            print (b), '"Enter Degree in integer Value and Minutes in Integer or Float values."'
        
        pass
    
    def subtract(self, angle):

        try:
            degree,minute = angle.split("d")
            
            
            if minute > 0:
                degree = int(degree) 
                degree = degree % 360
                minute = float(minute) 
                minute = round(minute,1)
                angle = degree+'d'+minute
                self.Angle = Angle - angle
                degree,minute = self.Angle.split("d")
                degree = degree % 360
                if minute == 30:
                    self.Angle = degree + 0.5
                elif minute == 60:
                    self.Angle = degree + 1
                else:
                    self.Angle = degree
                return self.Angle
            else:
                print "fail"
            
        except ValueError as b:
            print (b), '"Enter Degree in integer Value and Minutes in Integer or Float values."'


        pass
    
    def compare(self, angle):
        
            try:
                degree,minute = angle.split("d")
            
            
                if minute > 0:
                    degree = int(degree)
                    degree = degree % 360 
                    minute = float(minute) 
                    minute = round(minute,1)
                    angle = degree+'d'+minute
                    
                
                else:
                    print "fail"
                if self.Angle > angle:
                    return -1
                elif self.Angle == angle:
                    return 0
                else:
                    return 1
            
            except ValueError as b:
                print (b), '"Enter Degree in integer Value and Minutes in Integer or Float values."'

        
            pass
    
    def getString(self):
        
        degree,minute = self.angle.split("d")
            
            
        if minute > 0:
            degree = int(degree)
            degree = degree % 360 
            minute = float(minute) 
            minute = round(minute,1)
            minute = minute % 60
            self.angle = degree+'d'+minute
            return self.angle
                    
                
        else:
            print "fail"
        
        pass
    
    def getDegrees(self):
        
        degree,minute = self.angle.split("d")
            
            
        if minute > 0:
            degree = int(degree)
            degree = degree % 360 
            minute = float(minute) 
            minute = round(minute,1)
            minute = minute % 60
            self.angle = degree+' degrees and  '+minute+' minutes.'
            return self.angle
                    
                
        else:
            print "fail"
        
        pass
        
    x = setDegrees( 1 , 550 )
    x = setDegreesAndMinutes(1,'52d5.656')
    x = add(56)
        