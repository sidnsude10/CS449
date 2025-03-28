import unittest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from src.sos_game import SimpleSOS, GeneralSOS


class TestGameOver(unittest.TestCase):
    def setUp(self):
        
        self.simple_game = SimpleSOS(3)
        self.general_game = GeneralSOS(3)

    def test_simple_game_over(self):
        # simple mode should end immediately when an SOS is formed
        self.simple_game.makeMove(0, 0, "S")
        self.simple_game.makeMove(0, 1, "O")
        result = self.simple_game.makeMove(0, 2, "S")  

        self.assertEqual(result, "Game Over", "error: simple mode should end after first SOS.")

    def test_general_game_not_over(self):
        # general mode should not end until the board is full
        self.general_game.makeMove(0, 0, "S")
        self.general_game.makeMove(0, 1, "O")
        result = self.general_game.makeMove(0, 2, "S")  

        self.assertNotEqual(result, "Game Over", "error: general mode should not end after one SOS.")

    def test_general_game_over(self):
        # general mode should end when the board is completely filled
        moves = [
            (0, 0, "S"), (0, 1, "O"), (0, 2, "S"),
            (1, 0, "O"), (1, 1, "S"), (1, 2, "O"),
            (2, 0, "S"), (2, 1, "O"), (2, 2, "S"),
        ]
        for row, col, letter in moves:
            self.general_game.makeMove(row, col, letter)

        self.assertEqual(self.general_game.getGameState(), "Game Over - It's a Draw!", "error: general mode should end when board is full.")

    def test_invalid_move(self):
        # invalid moves should not change the board or turn
        self.simple_game.makeMove(1, 1, "S")
        starting_turn = self.simple_game.current_turn
        move_result = self.simple_game.makeMove(1, 1, "O")  

        self.assertFalse(move_result, "error: move should be rejected if cell is occupied.")
        self.assertEqual(self.simple_game.getCell(1, 1), "S", "error: cell should remain unchanged.")
        self.assertEqual(self.simple_game.current_turn, starting_turn, "error: turn should not switch after an invalid move.")

if __name__ == "__main__":
    unittest.main()
