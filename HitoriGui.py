import g2d
import time
from Constants  import *
from Menu       import Menu
from Boardgame  import BoardGame
from Utility    import File

class HitoriGui:
    def __init__(self, g: BoardGame):
        self._game        = g
        self._audio_menu  = g2d.load_audio("Audio/audio_menu.mp3")
        self._audio_black = g2d.load_audio("Audio/audio_black.mp3"), 
        self._audio_win   = g2d.load_audio("Audio/audio_win.mp3")
        self._menu        = Menu(CANVAS_DIM, CANVAS_DIM, self._audio_menu, self._game)

        self.start()
    #Method that starts the game
    def start(self):
        g2d.init_canvas((CANVAS_DIM, CANVAS_DIM))
        self._menu.startMenu(True)
        g2d.main_loop(self.tick)

    def tick(self):
        if self._menu.getMenuOn(): self._menu.drawMenu()
        elif not self._game.getStatus():
            self.keyControl() 
            self.update_buttons(True)
        else:
            File.deleteContinue(File)
            g2d.play_audio(self.getAudio("win"))
            self.winningBoard()        

    #Method that controls if you have pressed the mouse buttons
    def keyControl(self):                   
        if g2d.key_pressed(LEFTCLICK):  
            x, y = self.mousePos("black") 
            if x >= 0:  self._game.click(x, y, True)
        elif g2d.key_pressed(HELPCLICK):    self._game.circleAndBlack(True)
        elif g2d.key_pressed(ESC):          self.saveStatus()
        elif g2d.key_pressed(UNDO):         self._game.undo()
        elif g2d.key_pressed(AI):           self.nextMove()
        elif g2d.key_pressed(FINISH):       self.graphicResolve()    

    #Method that gets the position of the mouse     
    def mousePos(self, audio):
        x, y = g2d.mouse_position()
        if 0 < x < CANVAS_DIM and 0 < y < CANVAS_DIM:
            g2d.play_audio(self.getAudio(audio))
            return (int(x // (CANVAS_DIM/self._game.numRowsCols())), int(y // (CANVAS_DIM/self._game.numRowsCols())))
        return -1, -1

    #Method that saves the status to let the player continue the game in the future
    def saveStatus(self):
        File.writeContinue(File, self._game.getVal(), self._game.getGame(), self._game.getTimeX())
        self._menu.startMenu(True)

    #Method that draws at certain frequency the moves to win the game
    def graphicResolve(self):
        speed = SPEED/self._game.numRowsCols()
        while not self._game.getStatus(): 
            result = self._game.nextMove(True)
            self.update_buttons(False)
            g2d.update_canvas()
            if result == PRINT: 
                time.sleep(speed)  
            elif result == IMPOSSIBLE: 
                g2d.alert(MESSAGE_ERROR)      
                return 
        time.sleep(DELAY_WIN)
        g2d.update_canvas()
    
    #Method that draws next move only if it is possible
    def nextMove(self):
        if self._game.nextMove(False) == IMPOSSIBLE:
            g2d.alert(MOVE_ERROR)

    #Method that updates the canvas and all that is displayed on it 
    def update_buttons(self, seTime):
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        self.drawBoard(self._game.numRowsCols(), CANVAS_DIM, CANVAS_DIM)
        self.fillBoard()
        if seTime:  self._game.setTime()

    #Method that draws the board based on the number of cells retrieved from the Hitori object
    def drawBoard(self, num, w, h):                 
        if num == 0: return

        x = (w / num) * (num-1) 
        g2d.draw_line((x, 0), (x, h))
        g2d.draw_line((0, x), (h, x))

        self.drawBoard(num-1, w-(w/num), h)

    #Method that fills the board with the numbers' matrix retrieved from the Hitori object
    def fillBoard(self):                            
        s = CANVAS_DIM/self._game.numRowsCols()
        for y in range(self._game.numRowsCols()):
            for x in range(self._game.numRowsCols()):
                self.valueCheck(s, x, y)      

    #Method that checks a particular cell when filling the board and the draws a text, a circle or a rectangle based on the situation
    def valueCheck(self, s, x, y): 
        g2d.set_color((0,0,0))                 
        if self._game.game_at(x, y) == BLACK:
            g2d.set_color(COLOR_BLACK)   
            g2d.fill_rect((x*s, y*s,s,s))
            g2d.set_color((255,255,255)) 
        elif self._game.game_at(x, y) == CIRCLE:
            g2d.set_color(COLOR_CIRCLE)
            g2d.fill_circle((s*(x+1/2), s*(y+1/2)), s/2)
            g2d.set_color((255,255,255))
            g2d.fill_circle((s*(x+1/2), s*(y+1/2)), s/2*5/6) 
            g2d.set_color((0, 0, 0))
        g2d.draw_text_centered(str(self._game.value_at(x, y)), (s*(x+1/2), s*(y+1/2)), s/2)

    #Method that draws the winning frame
    def winningBoard(self):
        g2d.clear_canvas()
        w = CANVAS_DIM
        g2d.set_color(COLOR_BG)
        g2d.fill_rect((0,0,w, w))
        if self._game._newRecord == True:
            g2d.set_color(COLOR_RECORD)
            g2d.draw_text_centered(NEW_RECORD, (w/2, w/4), SIZE1*2)
        else:
            g2d.set_color(COLOR_FINISH)
            g2d.draw_text_centered(WON, (w/2, w/4), SIZE1*2)
            g2d.draw_text_centered('in', (w/2, w/4 + SIZE1*2), SIZE1*2)
        g2d.draw_text_centered(str(self._game.getTime())+" seconds", (w/2, w/4 + 4*SIZE1), SIZE1*2)
        self.buttonControl()

    #Method that manages the winning frame actions
    def buttonControl(self):
        w = CANVAS_DIM       
        x = g2d.mouse_position()[0]
        if 0 <= x < w/2:  
            g2d.set_color(COLOR_BACK) 
            g2d.draw_text_centered(EXIT, ((3/4)*w, 3/4*w), SIZE2)
            g2d.set_color(COLOR_RULES)
            g2d.draw_text_centered(MENU, (w/4, 3*w/4), SIZE2*2)
            if g2d.key_pressed(LEFTCLICK):
                self._game.endGame()
                self._menu.startMenu(False)
                g2d.pause_audio(self.getAudio("win"))
        else:
            g2d.set_color(COLOR_RULES)
            g2d.draw_text_centered(MENU, (w/4, 3*w/4), SIZE2)
            g2d.set_color(COLOR_BACK)
            g2d.draw_text_centered(EXIT, ((3/4)*w, 3/4*w), SIZE2*2)
            if g2d.key_pressed(LEFTCLICK):
                g2d.close_canvas()

    #Method that returns the right audio file based on the input
    def getAudio(self, string):
        if string == "menu":    return self._audio_menu
        elif string == "black": return self._audio_black
        elif string == "win":   return self._audio_win