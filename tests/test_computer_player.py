import unittest
from src.sos_game import GeneralSOS, ComputerPlayer

class TestComputerPlayer(unittest.TestCase):

    def test_computer_places_valid_move(self):
        game = GeneralSOS(3)
        player = ComputerPlayer("Blue", "S")
        empty_before = sum(row.count(" ") for row in game.board)

        player.make_move(game)
        empty_after = sum(row.count(" ") for row in game.board)

        self.assertEqual(empty_before - empty_after, 1, "Computer should fill one cell")

    def test_computer_uses_valid_letter(self):
        game = GeneralSOS(3)
        player = ComputerPlayer("Blue", "S")
        player.make_move(game)

        
        valid_letters = ["S", "O"]
        found = any(cell in valid_letters for row in game.board for cell in row)

        self.assertTrue(found, "Computer should place an S or O")

    def test_computer_does_not_overwrite(self):
        game = GeneralSOS(3)
        game.board[1][1] = "S" 
        player = ComputerPlayer("Blue", "S")
        player.make_move(game)

       
        self.assertEqual(game.board[1][1], "S", "Computer should not overwrite existing cell")

    def test_computer_game_reaches_end(self):
        game = GeneralSOS(3)
        player1 = ComputerPlayer("Blue", "S")
        player2 = ComputerPlayer("Red", "O")

        
        current_player = player1
        for _ in range(9):
            current_player.make_move(game)
            current_player = player2 if current_player == player1 else player1

        
        full = all(cell != " " for row in game.board for cell in row)
        self.assertTrue(full, "Game should end with a full board")

