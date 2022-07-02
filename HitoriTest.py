import unittest
from Hitori import Hitori
from Constants import *

class HitoriTest(unittest.TestCase):

    def test_HitoriTest(self):
        matrix =   [[4,5,2,3,2],
                    [4,5,5,2,3],
                    [5,2,3,4,3],
                    [3,3,1,2,2],
                    [1,3,4,1,5]]
        h = Hitori()
        h.startGame("5X5")
        h._values = [row[:] for row in matrix]
        h._game   = [row[:] for row in matrix]

        #BRUTAL TEST set my values test
        self.assertTrue(h._game[0][0] == 4 and h._values[0][1] == 5)

        #Test game_at
        self.assertTrue(h.game_at(0,0) == 4 and h.game_at(0,1) == 4)
        self.assertTrue(h.game_at(-1, 0) == OUT_OF_BOUNDS)
        self.assertTrue(h.game_at(16, 0) == OUT_OF_BOUNDS)
        self.assertTrue(h.game_at(0, -1) == OUT_OF_BOUNDS)
        self.assertTrue(h.game_at(0, 15) == OUT_OF_BOUNDS)

        #Test value_at, it doesn't need all control because i call it just i correct position
        self.assertTrue(h.value_at(0,0) == 4 and h.value_at(0,1) == 4)

        #Test play_at, it doesn't need all control because i call it just i correct position
        h.play_at(0,0)
        h.play_at(0,1)
        self.assertTrue(h.game_at(0,0) == BLACK and h.game_at(0,1) == BLACK)

        #Test flag_at, it doesn't need all control because i call it just i correct position
        h.flag_at(1,0)
        h.flag_at(1,1)
        self.assertTrue(h.game_at(1,0) == CIRCLE and h.game_at(1,1) == CIRCLE)

        #Test click in different situation
        h.click(0,4, False)
        self.assertTrue(h.game_at(0,4) == BLACK)
        
        h.click(0,4, False)
        self.assertTrue(h.game_at(0,4) == CIRCLE)

        h.click(0,4, False)
        self.assertTrue(h.game_at(0,4) == 1)

        #Test automatism in different situation
        h._game   = [row[:] for row in matrix]
        h.play_at(0,0)
        h.circleAndBlack(False)
        self.assertTrue(h.game_at(0,1) == CIRCLE and h.game_at(1,0) == CIRCLE)

        h._game   = [row[:] for row in matrix]
        h.flag_at(0,0)
        h.circleAndBlack(False)
        self.assertTrue(h.game_at(0,1) == BLACK and h.game_at(1,1) == CIRCLE)

        h._game   = [row[:] for row in matrix]
        h.circleAndBlack(False)
        self.assertTrue(h._game == matrix)

        #RuleCheck control if there are 2 black cells near
        h.play_at(0,0)
        h.play_at(0,1)
        self.assertTrue(h.ruleCheck(0,0))
        self.assertTrue(not h.ruleCheck(2,2))
        h.flag_at(0,1)
        self.assertTrue(not h.ruleCheck(0,0))

        #Test Lonely Number
        h.click(0,1, False)
        self.assertTrue(not h.lonelyNumber(0,1))
        self.assertTrue(h.lonelyNumber(3,2))

        #Test ChoiceX
        choiceTuple = [(x, y) for x in range(h.numRowsCols()) for y in range(h.numRowsCols()) if isinstance(h.game_at(y, x), int)]
        choiceX     = [x for x in range(len(choiceTuple))]

        self.assertTrue(len(choiceX) != 0)

        #Basic Test finished and test contiguity wrong
        h.play_at(1, 0)
        h.play_at(0, 1)
        self.assertFalse(h.finished())
        self.assertFalse(h.wrong())

        #Test contiguity finished and wrong
        h.play_at(4, 0)
        h.play_at(1, 2)
        h.play_at(1, 3)
        h.play_at(3, 3)
        h.play_at(4, 2)
        self.assertFalse(h.finished())
        self.assertFalse(h.wrong())

        #Test winning condition finished
        h._game   = [row[:] for row in matrix]
        h.play_at(0, 0)
        h.play_at(1, 1)
        h.play_at(4, 0)
        h.play_at(0, 4)
        h.play_at(1, 3)
        h.play_at(3, 3)
        h.play_at(4, 2)
        self.assertTrue(h.finished())

        #Tests that nextmove doesn't annotate wrong cells
        h._game   = [row[:] for row in matrix]
        h.nextMove(False)
        h.circleAndBlack(False)
        self.assertTrue(h.wrong())

        #Test if nextmove sees and impossible combination and stops 
        h._game   = [row[:] for row in matrix]
        h.play_at(1, 0)
        h.play_at(0, 1)
        self.assertTrue(h.nextMove(False) == IMPOSSIBLE)

        #Test if nextmove (True) finds the solution of the table
        h._game   = [row[:] for row in matrix]
        while not h.getStatus():
            h.nextMove(True)
        self.assertTrue(h.finished())

if __name__ == '__main__':unittest.main()
