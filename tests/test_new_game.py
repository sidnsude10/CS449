import unittest
from src.sos_game import SOSGame

class TestNewGame(unittest.TestCase):
    #Tests resetting the game correctly

    def test_board_reset(self):
        #makes sure starting a new game clears the board
        game = SOSGame(3)
        game.makeMove(0, 0, "S")  
        
        # restarting game
        game = SOSGame(3)
        for row in range(game.board_size):
            for col in range(game.board_size):
                self.assertEqual(game.getCell(row, col), " ", "Error: Board should be empty after restarting")

    def test_turn_reset(self):
        #make sure the first turn is always 'S' after restarting
        game = SOSGame(3)
        game.makeMove(0, 0, "S")  
        
        # restarting game
        game = SOSGame(3)
        
        self.assertEqual(game.current_turn, "S", "Error: First turn after restart should always be 'S'")

if __name__ == "__main__":
    unittest.main()
