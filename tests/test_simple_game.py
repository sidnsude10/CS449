import unittest
from src.sos_game import SimpleSOS  

class TestSimpleGame(unittest.TestCase):
    # tests for making moves in a simple game

    def setUp(self):
        # sets up a 3x3 SimpleSOS game before tests
        self.game = SimpleSOS(3)

    def test_valid_move(self):
        # making sure placing an 'S' or 'O' in an empty cell updates the board & switches turns
        starting_turn = self.game.current_turn  
        move_success = self.game.makeMove(1, 1, "S") 
        self.assertTrue(move_success, "error: valid move should be allowed.")
        self.assertEqual(self.game.getCell(1, 1), "S", "error: cell should contain 'S'.")
        self.assertNotEqual(self.game.current_turn, starting_turn, "error: turn should switch after a valid move.")

    def test_occupied_cell_move(self):
        # making sure placing a move in an occupied cell isn't allowed
        self.game.makeMove(1, 1, "O")  
        starting_turn = self.game.current_turn  
        move_success = self.game.makeMove(1, 1, "S")  
        self.assertFalse(move_success, "error: move in occupied cell should not be allowed.")
        self.assertEqual(self.game.getCell(1, 1), "O", "error: cell should remain unchanged.")
        self.assertEqual(self.game.current_turn, starting_turn, "error: turn should not change after an illegal move.")

    def test_out_of_bounds_move(self):  
        # making sure moves outside the board aren't placed and the turn stays the same  
        invalid_moves = [  
            (-1, -1),  # negative coordinates  
            (0, 3),    # row out of bounds  
            (3, 0),    # column out of bounds  
            (4, 4)     # both row and column out of bounds  
        ]  

        starting_turn = self.game.current_turn  

        for row, col in invalid_moves:  
            move_success = self.game.makeMove(row, col, "S")  
            self.assertFalse(move_success, f"error: move at ({row}, {col}) should not be allowed.")  
            self.assertEqual(self.game.current_turn, starting_turn, f"error: turn should not change after an invalid move.")  

    def test_sos_detection(self):
        # making sure the game ends when an SOS is formed
        self.game.makeMove(0, 0, "S")  
        self.game.makeMove(1, 0, "O")  
        result = self.game.makeMove(2, 0, "S")  

        self.assertEqual(result, "Game Over - Blue Wins!", "error: game should end when an SOS is formed.")

    def test_simple_game_draw(self):
        # making sure the game ends in a draw when the board is full and there's no SOS
        moves = [
            (0, 0, "S"), (0, 1, "O"), (0, 2, "S"),
            (1, 0, "S"), (1, 1, "S"), (1, 2, "O"),
            (2, 0, "O"), (2, 1, "S"), (2, 2, "O")
        ]
        
        for row, col, letter in moves:
            self.game.makeMove(row, col, letter)

        self.assertEqual(self.game.getGameState(), "Game Over - It's a Draw!", "error: the game should end in a draw if the board is full with no SOS.")

if __name__ == "__main__":  
    unittest.main()
