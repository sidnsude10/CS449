import unittest
from src.sos_game import GeneralSOS

class TestGeneralGame(unittest.TestCase):
    # tests for General Mode in the SOS game

    def setUp(self):
        # sets up a 3x3 GeneralSOS game before each test
        self.game = GeneralSOS(3)

    def test_valid_move(self):
        # making sure a valid move is placed correctly and turn switches
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
        # making sure a move outside the board isn't placed and turn stays the same
        invalid_moves = [(-1, -1), (0, 3), (3, 0), (4, 4)]
        starting_turn = self.game.current_turn

        for row, col in invalid_moves:
            move_success = self.game.makeMove(row, col, "S")
            self.assertFalse(move_success, f"error: move at ({row}, {col}) should not be allowed.")
            self.assertEqual(self.game.current_turn, starting_turn, "error: turn should not change after an invalid move.")

    def test_sos_counting(self):
        # making sure SOS formations are counted correctly in General Mode
        self.game.makeMove(0, 0, "S")
        self.game.makeMove(1, 0, "O")
        self.game.makeMove(2, 0, "S")  

        self.assertEqual(self.game.sos_count["Blue"], 1, "error: blue's SOS count should be 1.")

        self.game.makeMove(0, 1, "S")
        self.game.makeMove(1, 1, "O")
        self.game.makeMove(2, 1, "S")  

        self.assertEqual(self.game.sos_count["Blue"], 2, "error: blue's SOS count should be 2.")

    def test_general_game_winner(self):
        # making sure the player with the most SOS wins when the board is full
        moves = [
            (0, 0, "S"), (0, 1, "O"), (0, 2, "S"),  
            (1, 0, "S"), (1, 1, "O"), (1, 2, "S"),  
            (2, 0, "S"), (2, 1, "O"), (2, 2, "S"),  
            (0, 3, "O"), (1, 3, "S"), (2, 3, "O"),  
        ]
    
        for row, col, letter in moves:
            self.game.makeMove(row, col, letter)

        self.assertEqual(self.game.getGameState(), "Game Over - Blue Wins!", "error: the game should declare blue as the winner.")

    def test_general_game_draw(self):
        
        moves = [
            (0, 0, "S"), (0, 1, "O"), (0, 2, "S"),  
            (1, 0, "O"), (1, 1, "S"), (1, 2, "O"),  
            (2, 0, "S"), (2, 1, "O"), (2, 2, "S")  
        ]

        for row, col, letter in moves:
            self.game.makeMove(row, col, letter)

        self.assertEqual(self.game.getGameState(), "Game Over - It's a Draw!", "error: the game should end in a draw if SOS counts are equal.")

if __name__ == "__main__":
    unittest.main()
