import os
from random import choice
from os import path
from Constants import *

class File:
    #Method that sets the record in the corrispective record file
    def setRecord(self, name, time):
        os.makedirs(os.path.dirname(PATH_RECORDS+name), exist_ok=True)

        with open(PATH_RECORDS+name+".txt", "w") as file:
            file.write(time)

    #Method that gets the record from the corrispective record file
    def getRecord(self, name):
        try: 
            with open(PATH_RECORDS+str(name)+".txt", "r") as file:
                return float(file.readline())
        except: return float(INFINITY)
    
    #Method that checks if it is possible to continue the game
    def searchContinue(self): 
        if path.exists(PATH_CONTINUE+".txt"):
            MAIN_MENU[1] = "CONTINUE"
            return True 
        MAIN_MENU[1] = ""
        return False

    #Method that creates the continue file
    def writeContinue(self, matrixVal, matrixGame, time):
        File.valueWriter(File, matrixVal, "w")
        File.valueWriter(File, matrixGame, "a")
        with open(PATH_CONTINUE+".txt", "a") as file: file.write(str(time))

    #Method that writes numbers from a matrix in a file
    def valueWriter(self, values, type):
        with open(PATH_CONTINUE+".txt", type) as file:
            for i in range(len(values)):
                for j in range(len(values[i])-1):
                    file.write(str(values[i][j])+',')
                file.write(str(values[i][j+1])+"\n")        

    #Method that reads the continue file
    def readContinue(self):
        with open(PATH_CONTINUE+".txt", "r") as file:
            values = []
            for line in file:
                new_row = line.split(',')
                for i in range(len(new_row)):
                    if("\n" in new_row[i]): new_row[i] = new_row[i].rstrip("\n\r")
                    try:    new_row[i] = int(new_row[i])
                    except: pass
                    
                values.append(new_row)
                
            return File.splitMatrix(File, values), float(values[-1][0])
    
    #Method that spluts the matrix read from files
    def splitMatrix(self, values):
        lenght = int((len(values)-1)/2)
        matrixVal  = [[int(values[i][j]) for j in range(lenght)]for i in range(lenght)]
        matrixGame = [[values[i+lenght][j] for j in range(lenght)]for i in range(lenght)]

        return matrixVal, matrixGame

    #Method that deletes the continue file
    def deleteContinue(self): 
        if os.path.exists(PATH_CONTINUE+".txt"): os.remove(PATH_CONTINUE+".txt")
    
    #Function that retrieves the numbers matrix from the file name dependant from num
    def matrixReader(self, name) -> list:           
        with open(PATH_BOARDS+ name+".txt", "r") as file:
            values = []
            for line in file:
                new_row = line.split(',')
                for i in range(len(new_row)): 
                    new_row[i] = int(new_row[i])
                values.append(new_row)
            
            return File.changeMatrix(File,values)

    #Method that changes the matrix randomly(mirroring in it 1 or 2 times(the first time only inverting columns order and the second time also rows order))
    def changeMatrix(self, values):
        random = choice([0, 1, 2, 3])
        if random == 0: return values
        if random == 1: return [row[::-1] for row in values]
        if random == 2: return [[values[-1-i][j] for j in range(len(values[i]))] for i in range(len(values))]
        if random == 3: return [[values[-1-i][-1-j] for j in range(len(values[i]))] for i in range(len(values))]


'''
' Class that allows to go back in your moves....
'''          
class Undo():
    def __init__(self, matrixStart):
        self._matrixStart = matrixStart
        self._undo = []
        self._undo.append(matrixStart)

    def save(self, matrix): 
        if len(self._undo) == 0 or matrix != self._undo[-1]: 
            self._undo.append([row[:] for row in matrix])        

    def getUndo(self): 
        if len(self._undo) == 1: return self._matrixStart
        self._undo.pop()
        return self._undo[-1]