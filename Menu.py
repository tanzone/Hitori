import g2d
from Utility import File
from Constants import ( MAIN_MENU, LVL_MENU, RULES_MENU, SIZE1, HITORI, K, MATRICOLE, COLOR_RULES,
                        COLOR_BACK, COLOR_HOVER, COLOR_TITLE, COLOR_TEXT, COLOR_BG, COMMAND_MENU)

class Menu:

    def __init__(self, w, h, audioMenu, game):
        self._w, self._h = w, h
        self._menu       = False
        self._command    = False
        self._levels     = False
        self._continue   = False
        self._audio      = audioMenu
        self._game       = game

    def drawMenu(self):
        self.drawTitle()
        
        if   self._menu:    self.mouseZoom(g2d.mouse_position()[1], self._w, MAIN_MENU)
        elif self._levels:  self.mouseZoomLvls(g2d.mouse_position(), self._w, LVL_MENU)
        elif self._command: self.drawRules(g2d.mouse_position(), self._w, COMMAND_MENU)
        elif self._rules:   self.drawRules(g2d.mouse_position(), self._w, RULES_MENU)
        
        self.drawCopyright()

    #Method that draws the title of the menu
    def drawTitle(self):
        g2d.clear_canvas()
        g2d.set_color(COLOR_BG)
        g2d.fill_rect((0,0,self._w, self._h))
        g2d.set_color(COLOR_TITLE)
        g2d.draw_text_centered(HITORI, (self._w/2, self._w/6), SIZE1*5/2)
        g2d.draw_line((20, self._w/6 + SIZE1), (self._w-20, self._w/6 + SIZE1))

    #Method that magnifies the text the mouse is positioned on
    def mouseZoom(self, pos, w, choice):
        for i in range(len(choice)):
            if i == len(choice)-1: g2d.set_color(COLOR_BACK)
            else: g2d.set_color(COLOR_TEXT)      
            if (2/5)*w + i*K - SIZE1 <= pos < (2/5)*w + (i+1)*K - SIZE1:
                if not i == len(choice)-1:  g2d.set_color(COLOR_HOVER)
                g2d.draw_text_centered(choice[i], (w/2, (2/5)*w+i*K), SIZE1*2)
                if g2d.key_pressed("LeftButton"):
                    self.mousePressed(i)
            else: g2d.draw_text_centered(choice[i], (w/2, (2/5)*w+i*K), SIZE1)

    #Same as last method but for the levels menu
    def mouseZoomLvls(self, pos, w, choice):
        for i in range(2):
            for j in range(len(choice)//2):
                if ((2/5)*w + j*K - SIZE1 <= pos[1] < (2/5)*w + (j+1)*K - SIZE1) and (i*(w/2) < pos[0] < (w/2)*(i+1)):
                    g2d.set_color(COLOR_HOVER)
                    g2d.draw_text_centered(choice[j+((len(choice)//2)*i)], ((w/4)*(i*2+1), (2/5)*w+j*K), SIZE1*2)
                    if g2d.key_pressed("LeftButton"):
                        self.mousePressed(j+(len(choice)//2)*i)
                else: 
                    g2d.set_color(COLOR_TEXT)
                    g2d.draw_text_centered(choice[j+((len(choice)//2)*i)], ((w/4)*(i*2 +1), (2/5)*w+j*K), SIZE1)
        
        self.buttonBack(pos, w, choice)

    #Method that manages the clicks in the various menus
    def mousePressed(self, choice):
        g2d.play_audio(self._audio)
        if     self._menu and choice == 0: self.setChoice(False, True, False, False)
        elif   self._menu and choice == 1 and self._continue: self.functionToContinue()
        elif   self._menu and choice == 2: self.setChoice(False, False, True, False)
        elif   self._menu and choice == 3: self.setChoice(False, False, False, True)
        elif   self._menu and choice == 4: g2d.close_canvas()

        elif self._levels and choice == -1: self.setChoice(True, False, False, False)
        elif self._levels:                  self.functionToPlay(LVL_MENU[choice])             

        elif self._command and choice == -1:  self.setChoice(True, False, False, False)
        elif self._rules   and choice == -1:  self.setChoice(True, False, False, False)             

    #Method that starts the game
    def functionToPlay(self, choice):
        if choice != "":
            File.deleteContinue(File)
            self.setChoice(False, False, False, False)
            self._game.startGame(choice)

    #Method that continues the game
    def functionToContinue(self):
        val, timeX = File.readContinue(File)
        num = str(len(val[0])) + "X" + str(len(val[0]))
        self.setChoice(False, False, False, False)
        self._game.continueGame(num, val[0], val[1], timeX)

    #Method that draws the rules
    def drawRules(self, pos, w, choice):
        g2d.set_color(COLOR_RULES)
        for i in range(len(choice)-1):
            g2d.draw_text(choice[i], (w/12, (1/3)*w+i*(3*K/4)), SIZE1*2/3)
        self.buttonBack(pos, w, LVL_MENU)

    #Method that manages the back button
    def buttonBack(self, pos, w, choice):
        g2d.set_color(COLOR_BACK)
        if ((2/5)*w + (len(choice)//2)*K - SIZE1 <= pos[1] < (2/5)*w + (len(choice)//2+1)*K - SIZE1):
            g2d.draw_text_centered(choice[-1], ((w/2), (2/5)*w+(len(choice)//2)*K), SIZE1*2)
            if g2d.key_pressed("LeftButton"):self.mousePressed(-1)
        else: g2d.draw_text_centered(choice[-1], ((w/2), (2/5)*w+(len(choice)//2)*K), SIZE1)

    #Draws the copyright line in the menu
    def drawCopyright(self):
        g2d.set_color(COLOR_TITLE)
        g2d.draw_line((0, self._h-20), (self._w, self._h-20))
        g2d.draw_text_centered("   @Copyright by  :  " + MATRICOLE, (self._w/2, self._h-(20/2)), 17)

    #Method that sets all attributes to start the menu
    def startMenu(self, menu): 
        self._continue = File.searchContinue(File)
        if menu: self._menu = True
        else: self._levels  = True
        
    #Method that sets the choice based on input
    def setChoice(self, menu, levels, command, rules):
        self._menu    = menu
        self._levels  = levels
        self._command = command
        self._rules   = rules

    def getMenuOn(self) -> bool: return self._menu or self._levels  or self._command or self._rules
