class Angle():
    
    def __init__(self):
        #self.angle = ...       set to 0 degrees 0 minutes
        self.angle = 0
           
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
                self.angle = self.angle * 60
                self.angle = abs(self.angle)
                self.angle = round(self.angle, 1)
                self.angle = self.angle/60
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
                
                degreenminute = angleString.split("d")
                self.degree = int(degreenminute[0])
                self.minute = float(degreenminute[1])
                if self.minute < 0:
                    raise ValueError("Angle.setDegreesAndMinutes:    Minutes cannot be negative.")
                
                countdec = degreenminute[1].find(".")
                if len(degreenminute[1]) - countdec == 2 :
                    pass
                else:
                    raise ValueError("Angle.setDegreesandMinutes:    Minutes can contain only one decimal places.")
                
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
            
        except:
            raise ValueError("Angle.setDegreesAndMinutes:   Enter Data not valid")

            
    def add(self, angle = None):


        if not(isinstance(angle, Angle)):
            raise ValueError("Angle.add:")
        else:
            self.angle += angle.getDegrees()
            self.angle %= 360
            return self.angle
            
    def subtract(self, angle = None):
 
        if not(isinstance(angle, Angle)):
            raise ValueError("Angle.subtract:")
        else:
            self.angle -= angle.angle
            self.angle %= 360
            return self.angle
     
    def compare(self, angle = None):
        if not(isinstance(angle, Angle)):
            raise ValueError("Angle.compare: Not instance of Angle")
        if self.angle == angle.getDegrees():
            return 0
        elif self.angle > angle.getDegrees():
            return 1
        else:
            return -1
       
             
            
    def getString(self):
         
       degree = int(self.angle)
       minute = self.angle - degree
       minute *= 60
       minute = round(minute,1)
       degree = str(degree)
       minute = str(minute)
       return degree + 'd' + minute
                     
                 
        
     
    def getDegrees(self):
        
            return self.angle
        