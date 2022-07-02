### CONSTANTS FOR THE HITORI GAME ###

CANVAS_DIM     = 600

BLACK          = '#'
CIRCLE         = '!'
OUT_OF_BOUNDS  = 'Error'

LEFTCLICK      = 'LeftButton'
ESC            = "Escape"
HELPCLICK      = "h"
UNDO           = "r"
AI             = "Spacebar"
FINISH         = "f"

PRINT          = "PRINT"
IMPOSSIBLE     = "IMPOSSIBLE"




### CONSTANTS FOR TEXT DRAWING ###

WON            = '!! YOU WON !!'
MENU           = 'MENU'
EXIT           = 'QUIT'
HITORI         = 'HITORI'
NEW_RECORD     = '!! New Record !!'
SIZE1          = CANVAS_DIM/16
SIZE2          = CANVAS_DIM/24
K              = SIZE1*2
MAIN_MENU      = ["PLAY", "CONTINUE", "COMMANDS", "RULES", "QUIT"]
LVL_MENU       = ["5X5", "6X6","8X8", "9X9", "10X10", "12X12", "15X15", "20X20", "BACK"]
COMMAND_MENU   = ["1] Press [Esc] to return to the menu from game", "2] Press [SPACE] to get the next hard move", "3] Press ["+ HELPCLICK.upper() +"] to get instant Help", 
                  "4] Press ["+UNDO.upper()+"] to Return last move", "5] Press ["+FINISH.upper()+"] to Finish using AI", "BACK"]
RULES_MENU     = ["Click 1 time to blacken the cell","Click 2 times to circle the cell",  "No black cells side by side", "No repetition of numbers in row or column", "Contiguous white cells",  "BACK"]


MATRICOLE      = "307720 - 308214"
MESSAGE_ERROR  = "!- IMPOSSIBLE WIN WITH THIS BOARD -! PRESS [R] to Return back to last move"
MOVE_ERROR     = "One of your moves is wrong"

PATH_RECORDS  = "Records/record"
PATH_BOARDS   = "Boards/board"
PATH_CONTINUE = "Continue/Continue"
INFINITY      = -1

SPEED         = 1.5
DELAY_WIN     = 3
COLOR_BG      = (34, 40, 49)
COLOR_TITLE   = (255, 166, 50)
COLOR_BACK    = (237,51,48)
COLOR_HOVER   = (254, 207, 0)
COLOR_TEXT    = (238, 238, 238)
COLOR_RULES   = (238, 238, 238)
COLOR_RECORD  = (70, 209, 78)
COLOR_FINISH  = (254, 207, 0)

COLOR_BLACK   = (50, 50, 50)
COLOR_CIRCLE  = COLOR_HOVER#(0, 173, 181)




