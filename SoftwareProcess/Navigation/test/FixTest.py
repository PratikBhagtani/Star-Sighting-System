'''
Created on Oct 11, 2016

@author: pRaTiK BhAgTaNi
'''
import unittest
import Navigation.prod.Fix as Fii


class FixTest(unittest.TestCase):
#     
#     Acceptance Tests 
#         100 Analysis constructor
#             inputs and outputs
#                 inputs ->  logfile
#                 outputs -> state change
#         Happy Path
#             nominal case -> Fix(logFile)
#         Sad Path
#             invalid parameter


    def test100_010_ShouldCreateInstance(self):
        self.assertIsInstance(Fii.Fix('logFile.txt'), Fii.Fix)

    def test100_020_ShouldWriteInFile(self):
        expected = "Log:  2016-10-16 Log Starting"
        Fii.Fix('logFile.txt')
        file = open('logFile.txt', 'r')
        for lines in file:
            rec = lines
    
    def test200_010_ShouldCreateInput(self):
        fxi = Fii.Fix()
        self.assertEqual(fxi.setSightingFile('CA02.xml'), 'CA02.xml')
        
    
    

        
        
    