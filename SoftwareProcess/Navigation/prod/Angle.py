class Angle():
    
    def __init__(self):
        #self.angle = ...       set to 0 degrees 0 minutes
        self.angle = '0d0'
           
    def setDegrees(self,degrees = 0.0):
                if(isinstance(degrees, float)):
                    pass
                    
                elif(isinstance(degrees, int)):
                    degrees = float(degrees)
                else:
                    raise ValueError('Angle.setDegrees:  the value entered for degrees should be an integer or float')
                    
                while degrees < 0.0:
                    degrees += 360
                    
              
                self.angle = degrees % 360
                self.angle = abs(self.angle)
                return self.angle

    
    def setDegreesAndMinutes(self,angleString):
        fname = "Angle.setDegreesAndMinutes: "
        try:
            if angleString[0] == "d":
                raise ValueError(fname + "Degree not Entered")
            
            elif (not(isinstance(angleString, str))):
                raise ValueError(fname + "Degree not Entered")
            
            elif angleString.find("d") == False:
                raise ValueError(fname + "Degree not Entered")
            
            else:
                print "executed"
                degreenminute = angleString.split("d")
                self.degree = (degreenminute[0])
                self.minute = float(degreenminute[1])
                
                if self.degree == int(self.degree):
                    raise ValueError(fname + "Degree not Entered")
                self.degree = int(self.degree)
                
                if self.minute != round(self.minute,1):
                    raise ValueError('Angle.setDegreesAndMinutes:')
                    self.minute = round(self.minute, 1)
                if self.degree < 0:
                    self.angle = self.degree - self.minute / 60
                else:
                    self.angle = self.degree + self.minute / 60
                self.angle = self.angle % 360
                while self.angle < 0:
                    self.angle += 360
            return self.angle  
            
        except AssertionError as e:
            print (e)

            
    def add(self, angle):
         
        try:
            degreenminute = self.angle.split("d")
            self.degree = int(degreenminute[0])
            self.minute = float(degreenminute[1])
             
            if self.minute > 0:
                self.degree = int(self.degree)
                self.degree = self.degree % 360 
                self.minute = float(self.minute) 
                self.minute = round(self.minute,1)
                angle = self.degree+'d'+self.minute
                self.Angle = Angle + angle
                degreenminute = self.Angle.split("d")
                self.degree = int(degreenminute[0])
                self.minute = float(degreenminute[1])
                self.degree = self.degree % 360
                if self.minute == 30:
                    self.angle = self.degree + 0.5
                elif self.minute == 60:
                    self.angle = self.degree + 1
                else:
                    self.angle = self.degree
                return self.angle
             
             
            else:
                print "fail"
             
        except ValueError as b:
            print (b), '"Enter Degree in integer Value and Minutes in Integer or Float values."'
 
     
    def subtract(self, angle):
 
        try:
            degreenminute = angle.split("d")
             
             
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
     
    def getDegrees(self):
        
            return self.angle
        