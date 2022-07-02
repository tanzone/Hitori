from Boardgame import BoardGame
from Constants import BLACK, CIRCLE, OUT_OF_BOUNDS, PRINT, IMPOSSIBLE
from Utility import File, Undo
from random import choice
import time

class Hitori(BoardGame):
    def __init__(self):
        self._num, self._values, self._game, self._bool_matrix = None, None, None, None
        self._count, self._bool_count, self._time              = 0, 0, 0
        self._isFinished, self._newRecord, self._undo          = False, False, None
    
    #Method that sets all Hitori's attributes to be able to start the game
    def startGame(self, num):
        self._num    = num
        self._values = File.matrixReader(File, num) #Unchanging Matrix
        self._game   = [row[:] for row in self._values]  #Game Matrix
        self._undo   = Undo(self._values)                #Undo Matrix
        self._time   = time.time()

    #Method that sets all Hitori's attributes to be able to continue the previous game
    def continueGame(self, num, matrixVal, matrixGame, timeX):
        self._num    = num
        self._values = matrixVal           #changing Matrix
        self._game   = matrixGame          #Game Matrix
        self._undo   = Undo(self._game)    #Undo Matrix
        self._time   = time.time() - timeX   

    #Method that empties all Hitori's attributes to be able to start a new game
    def endGame(self):                                                         
        self._num, self._values, self._game, self._bool_matrix    = None, None, None, None
        self._count, self._bool_count, self._time                 = 0, 0, 0
        self._isFinished, self._newRecord, self._undo             = False, False, None

    #Method that returns game status at a particular cell if possible or "Error" if the cell doesn't exist
    def game_at(self, x: int, y: int) -> str:       
        if 0 <= x < len(self._game[0]) and 0 <= y < len(self._game):
            return self._game[y][x]
        return OUT_OF_BOUNDS
    
    #Method that returns the initial string contained in a cell before the game started
    def value_at(self, x: int, y: int) -> str: 
        return self._values[y][x]
    
    #Method that returns the value of the selected cell from the boolean matrix, only if the values are in range 
    def bool_at(self, x, y):
        if 0 <= x < len(self._bool_matrix[0]) and 0 <= y < len(self._bool_matrix):
            return self._bool_matrix[y][x]
        return OUT_OF_BOUNDS

    #Method sets the game matrix one move backward
    def undo(self): self._game = [row[:] for row in self._undo.getUndo()] 

    #Method that blackens a cell if is white and whitens a cell if is black     
    def play_at(self, x: int, y: int):  self._game[y][x] = BLACK

    #Method that circles a cell if is white and whitens a cell if si circled
    def flag_at(self, x: int, y: int):  self._game[y][x] = CIRCLE

    #Method that recognizes the situation of a cell and decides between blackening it, circling it or whitening it 
    def click(self, x, y, save):
        if isinstance(self.game_at(x, y),int):  self.play_at(x,y)
        elif self.game_at(x, y) == BLACK:       self.flag_at(x,y)
        elif self.game_at(x, y) == CIRCLE:      self._game[y][x] = self._values[y][x]
        if save: self._undo.save(self._game)
        self.setStatus()      
    
    '''
    AUTO MOVES:

    The next four methods recursively annotate all the possible cells, based on the set conditions
    (If a cell is black the four contiguous to it must be circled and if a number is circled on a row or column then
    the copies of it in the same row or column must be black)
    '''

    def circleAndBlack(self, save):
        for i in range(0, self.numRowsCols()):
            for j in range(0, self.numRowsCols()):
                if self.game_at(j, i) == CIRCLE: 
                    self.functionBlack(j, i)
        self.functionCircle()
        if save: self._undo.save(self._game)
        self.setStatus() 

    def functionBlack(self, j, i):
        for k in range(0, self.numRowsCols()):
            if self.value_at(j, i) == self.value_at(k, i) and self.game_at(k, i) != CIRCLE and k != j:
                self._game[i][k] = BLACK
            if self.value_at(j, i) == self.value_at(j, k) and self.game_at(j, k) != CIRCLE and k != i:
                self._game[k][j] = BLACK

    def functionCircle(self):
        for i in range(0, self.numRowsCols()):
            for j in range(0, self.numRowsCols()):
                if self.game_at(j, i) == BLACK:
                    self.circleInCircle(j+1, i)
                    self.circleInCircle(j-1, i)
                    self.circleInCircle(j, i+1)
                    self.circleInCircle(j, i-1)

    def circleInCircle(self, j, i):
        if isinstance(self.game_at(j, i), int):
            self.flag_at(j, i)
            self.circleAndBlack(False)

    #Method that checks if a particular black cell has another one near her
    def ruleCheck(self, i, j) -> bool:              
        return (self.game_at(j, i)   == BLACK and 
               (self.game_at(j, i+1) == BLACK or self.game_at(j, i-1) == BLACK or self.game_at(j+1, i) == BLACK or self.game_at(j-1, i) == BLACK))

    #Method that checks if the player has won by looking if there's a repeated number in rows or columns                    
    def finished(self):                             
        self._count, self._bool_count   = 0, 0
        self._bool_matrix               = [[False for i in range(self.numRowsCols())]for j in range(self.numRowsCols())]
        
        for i in range(self.numRowsCols()):
            for j in range(self.numRowsCols()):
                if self.game_at(j, i) != BLACK and self.game_at(j, i) != OUT_OF_BOUNDS:    
                    self._count += 1
                #Controls if there are 2 or more black cells near
                if self.ruleCheck(i, j): return False
                #Controls if there are 2 or more equal numbers in row or in column
                for k in range(j, self.numRowsCols()):

                    if self.game_at(j, i) != BLACK and self.game_at(j, i) != OUT_OF_BOUNDS and self.game_at(k, i) != OUT_OF_BOUNDS and self.game_at(k, i) != BLACK and k != j:
                        if self.value_at(j, i) == self.value_at(k, i):
                            return False

                    if self.game_at(i, j) != BLACK and self.game_at(i, j) != OUT_OF_BOUNDS and self.game_at(i, k) != OUT_OF_BOUNDS and self.game_at(i, k) != BLACK and k != j:
                        if self.value_at(i, j) == self.value_at(i, k):
                            return False
        #Contiguity of the cells        
        self.checkWhiteCells(1, 0, 0, 0)
        if self._bool_count == self._count:
            self._isFinished = True
            return True
    
    #Recursion that checks if all the white cells are contiguous
    def checkWhiteCells(self, j, i, x, y):
        if self.bool_at(j, i) == False and self.game_at(j, i) != BLACK and self.game_at(j, i) != OUT_OF_BOUNDS:
            self._bool_matrix[i][j] = True
            self._bool_count        += 1
            for dj, di in ((j+1, i), (j-1, i), (j, i+1), (j, i-1)):
                self.checkWhiteCells(dj, di, j, i)
        elif self.game_at(j, i) == BLACK:
            self.checkWhiteCells(x, y, j, i)

    #Method used in the nextMove methods it checks if there is an immediate error in the combination
    def wrong(self):
        self._count, self._bool_count = 0, 0
        self._bool_matrix             = [[False for i in range(self.numRowsCols())]for j in range(self.numRowsCols())]

        for i in range(self.numRowsCols()):
            for j in range(self.numRowsCols()): 
                if self.game_at(j, i) != BLACK and self.game_at(j, i) != OUT_OF_BOUNDS: 
                    self._count += 1  
                if self.ruleCheck(i, j): return False
                if self.game_at(j, i) == CIRCLE:
                    if self.circleControl(j, i): return False
             
        self.checkWhiteCells(1, 0, 0, 0)
        return self._bool_count == self._count
    
    #Method that checks if a number is repeatedly circled on the same row or column
    def circleControl(self, j, i):
        for k in range(self.numRowsCols()):
            if self.game_at(k, i) == CIRCLE and k != j:
                if (self.value_at(k, i) == self.value_at(j, i)): return True
            if self.game_at(j, k) == CIRCLE and k != i:
                if (self.value_at(j, k) == self.value_at(j, i)): return True

    #Method that called with finish = False calculates the next exact move and stops, while called with finish = True
    #calculates all the moves necessary to resolve the game. If it can't get the solution gives an error
    def nextMove(self, finish):
        firstStatus = [row[:] for row in self._game]
        choiceTuple = [(x, y) for x in range(self.numRowsCols()) for y in range(self.numRowsCols()) if isinstance(self.game_at(y, x), int)]
        choiceX     = [x for x in range(len(choiceTuple))]
        if len(choiceX) == 0: return IMPOSSIBLE
        
        self.circleAndBlack(False)
        if not self.wrong():
            self._game = [row[:] for row in firstStatus]
            return IMPOSSIBLE
        self._game = [row[:] for row in firstStatus]
        
        i, j, x = self.choiceX(choiceX, choiceTuple)
    
        if self.lonelyNumber(i, j): 
            self._game[i][j] = CIRCLE
            return self.moveForFinish(finish)

        return self.resolve(firstStatus, finish, i, j, x, choiceX)

    #Method that looks for isolated numbers in rows and columns
    def lonelyNumber(self, i, j):
        for k in range(self.numRowsCols()):
            if (self.game_at(k, i) == self.game_at(j, i) or (self.game_at(j, i) == self.value_at(k, i) and self.game_at(k, i) == CIRCLE)) and k != j: return False
            if (self.game_at(j, k) == self.game_at(j, i) or (self.game_at(j, i) == self.value_at(j, k) and self.game_at(j, k) == CIRCLE)) and k != i: return False
        return True 

    #Involved with the nextMove method
    def resolve(self, firstStatus, finish,i, j, x, choiceX):
        saved = [row[:] for row in self._game]
        if    self.tryMove(i, j, BLACK, CIRCLE, saved): return self.moveForFinish(finish)
        elif  self.tryMove(i, j, CIRCLE, BLACK, saved): return self.moveForFinish(finish)
        else: 
            self._game = [row[:] for row in saved] 
            choiceX.append(x)
        return PRINT

    #Method that returns a random choice from an array of tuples
    def choiceX(self, choiceX, choiceTuple):
        x = choice(choiceX)
        choiceX.remove(x)
        return choiceTuple[x][0], choiceTuple[x][1], x

    #Method that tries to annotate a particular cell and checks if the combination is wrong
    def tryMove(self, i, j, typeMove, otherType, saved):
        self._game[i][j] = typeMove
        self.circleAndBlack(False)
        if not self.wrong(): 
            self._game = [row[:] for row in saved]
            self._game[i][j] = otherType 
            return True
        self._game = [row[:] for row in saved]
        return False          

    def moveForFinish(self, finish):
        if finish: self.circleAndBlack(False)
        else:      self.setStatus()
        return PRINT


    '''Setters and getters for all the necessary attributes'''

    def getTimeX(self):         return "%.2f" %(float(time.time()) - float(self._time))
    def getTime(self):          return self._time
    def getVal(self):           return self._values
    def getGame(self):          return self._game
    def getStatus(self):        return self._isFinished
    def numRowsCols(self):      return len(self._values)
    def setTimeX(self, timeX):  self._time       = timeX
    def setVal(self, matrix):   self._values     = matrix
    def setGame(self, matrix):  self._game       = matrix
    def setStatus(self):        self._isFinished = self.finished()
    
    def setTime(self):
        if self.getStatus():
            self._time = self.getTimeX()
            record = File.getRecord(File, str(self._num))
            if float(self._time) < record or record < 0:
                File.setRecord(File, str(self._num), self._time)
                self._newRecord = True