import unittest
from src.sos_game import SimpleSOS, GeneralSOS, SOSGame  

class TestGameMode(unittest.TestCase):
    # tests selecting simple or general game mode
    def test_simple_mode(self):
        # initializes SimpleSOS game
        game = SimpleSOS(3)
        self.assertIsInstance(game, SimpleSOS, "Error: Simple mode should initialize a SimpleSOS instance.")

    def test_general_mode(self):
        # initializes GeneralSOS game
        game = GeneralSOS(3)
        self.assertIsInstance(game, GeneralSOS, "Error: General mode should initialize a GeneralSOS instance.")

    def test_invalid_mode(self):
        # makes sure an invalid mode selection does not make a valid instance
        with self.assertRaises(TypeError, msg="Error: Invalid mode selection should raise TypeError."):
            raise TypeError("Invalid mode selection. Must be 1 (Simple) or 2 (General).")  

    def test_board_size_check(self):
        # SimpleSOS and GeneralSOS reject invalid board sizes
        with self.assertRaises(ValueError, msg="Error: SimpleSOS should reject board sizes less than 3."):
            SimpleSOS(2)

        with self.assertRaises(ValueError, msg="Error: GeneralSOS should reject board sizes less than 3."):
            GeneralSOS(1)

if __name__ == "__main__":
    unittest.main()


