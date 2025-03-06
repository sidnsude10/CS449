import unittest
from src.sos_game import GeneralSOS

class TestGeneralGame(unittest.TestCase):
    #Tests making a move in general mode

    def setUp(self):
        #initialize a general mode game before each test
        self.game = GeneralSOS(3)

    def test_valid_move(self):
        #makes sure a valid move places S/O and switches turns
        move_success = self.game.makeMove(1, 1, "S")
        self.assertTrue(move_success, "Valid move should be successful.")
        self.assertEqual(self.game.getCell(1, 1), "S", "Cell should contain 'S' after valid move.")
        self.assertEqual(self.game.current_turn, "O", "Turn should switch after a valid move.")

    def test_occupied_cell(self):
        #makes sure a move cannot be placed in an occupied cell
        self.game.makeMove(0, 0, "S")  
        move_success = self.game.makeMove(0, 0, "O")
        self.assertFalse(move_success, "Move should fail if cell is already occupied")
        self.assertEqual(self.game.getCell(0, 0), "S", "Cell should remain unchanged")

    def test_out_of_bounds_move(self):
        #makes sure a move cannot be placed outside the board
        move_success = self.game.makeMove(3, 0, "S")  # out of bounds for 3x3 dimension
        self.assertFalse(move_success, "Error: Move should fail if out of bounds")

if __name__ == "__main__":
    unittest.main()

