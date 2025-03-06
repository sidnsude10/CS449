import unittest
from src.sos_game import SimpleSOS  

class TestSimpleGame(unittest.TestCase):
    #Tests for making moves in a simple game

    def setUp(self):
        #initializes a 3 dimension SimpleSOS game before tests
        self.game = SimpleSOS(3)

    
    def test_valid_move(self):
        #making it so that placing a S or a O in an empty cell should update the board & switch turns
        starting_turn = self.game.current_turn  
        move_success = self.game.makeMove(1, 1, "S") 
        self.assertTrue(move_success, "Error: Valid move should be allowed.")
        self.assertEqual(self.game.getCell(1, 1), "S", "Error: Cell should contain 'S'.")
        self.assertNotEqual(self.game.current_turn, starting_turn, "Error: Turn should switch after a valid move.")

    
    def test_occupied_cell_move(self):
        #making it so that placing a S or a O in an occupied cell shouldn't be allowed
        self.game.makeMove(1, 1, "O")  
        starting_turn = self.game.current_turn  
        move_success = self.game.makeMove(1, 1, "S")  
        self.assertFalse(move_success, "Error: Move in occupied cell should not be allowed.")
        self.assertEqual(self.game.getCell(1, 1), "O", "Error: Cell should remain unchanged.")
        self.assertEqual(self.game.current_turn, starting_turn, "Error: Turn should not change after an illegal move.")

    
    # Originally AI generated with some changes made
    def test_out_of_bounds_move(self):  
        """Ensure a move outside the board is not placed and turn remains unchanged."""  
        invalid_moves = [  
            (-1, -1),  # Negative coordinates  
            (0, 3),    # Row out of bounds  
            (3, 0),    # Column out of bounds  
            (4, 4)     # Both row and column out of bounds  
        ]  

        starting_turn = self.game.current_turn  # Track initial turn  

        for row, col in invalid_moves:  
            move_success = self.game.makeMove(row, col, "S")  # Attempt invalid move  
            self.assertFalse(move_success, f"Error in test_out_of_bounds_move: Move at ({row}, {col}) should not be allowed.")  
            self.assertEqual(self.game.current_turn, starting_turn, f"Error in test_out_of_bounds_move: Turn should not change after an invalid move.")  

if __name__ == "__main__":  
    unittest.main()
