from abc import ABC, abstractmethod
import random

class SOSGame:
    def __init__(self, board_size):
        if board_size < 3:
            raise ValueError("Board size must be at least 3x3.")
        
        self.board_size = board_size
        self.board = [[" " for _ in range(board_size)] for _ in range(board_size)]
        self.current_turn = "S"  
        self.sos_count = {"S": 0, "O": 0}  

    def getCell(self, row, column):
        if 0 <= row < self.board_size and 0 <= column < self.board_size:
            return self.board[row][column]
        return None  

    def validateMove(self, row, column, letter):
        if not (0 <= row < self.board_size and 0 <= column < self.board_size):
            return False  
        if self.board[row][column] != " " or letter not in ("S", "O"):
            return False  
        return True

    def makeMove(self, row, column, letter):
        if not self.validateMove(row, column, letter):
            return False  

        self.board[row][column] = letter  
        return True  

    def switch_turn(self):
        self.current_turn = "O" if self.current_turn == "S" else "S"

    def checkForSOS(self, row=None, column=None):
        directions = [
            (0, 1),   # right
            (1, 0),   # down
            (1, 1),   # down-right
            (-1, 1),  # up-right
            (0, -1),  # left
            (-1, 0),  # up
            (-1, -1), # up-left
            (1, -1)   # down-left
        ]

        found_sos = 0

        # Simple mode
        if row is not None and column is not None:
            for dr, dc in directions:
                try:
                    if (
                        self.getCell(row - dr, column - dc) == "S" and
                        self.getCell(row, column) == "O" and
                        self.getCell(row + dr, column + dc) == "S"
                    ):
                        found_sos += 1
                except IndexError:
                    continue
            return found_sos

        # General mode
        for r in range(self.board_size):
            for c in range(self.board_size):
                for dr, dc in directions:
                    try:
                        if (
                            self.getCell(r - dr, c - dc) == "S" and
                            self.getCell(r, c) == "O" and
                            self.getCell(r + dr, c + dc) == "S"
                        ):
                            found_sos += 1
                    except IndexError:
                        continue

        return found_sos
  

    def getGameState(self): 
        if isinstance(self, SimpleSOS):
            if self.isGameOver():  
                return "Game Over - It's a Draw!"

            for r in range(self.board_size):
                for c in range(self.board_size):
                    if self.checkForSOS(r, c) > 0:
                        return f"Game Over - {self.current_player_name} Wins!"


            return "Game In Progress"

        if isinstance(self, GeneralSOS):
            if not self.isGameOver():
                return "Game In Progress"  

        if self.blue_score > self.red_score:
            return "Game Over - Blue Wins!"
        elif self.red_score > self.blue_score:
            return "Game Over - Red Wins!"
        else:
            return "Game Over - It's a Draw!"

             

        return "Game In Progress"

    def isGameOver(self):
        return all(cell != " " for row in self.board for cell in row)


class SimpleSOS(SOSGame):
    def makeMove(self, row, col, letter):
        if not self.validateMove(row, col, letter):
            return False

        self.board[row][col] = letter
        sos_count = self.checkForSOS(row, col)

        if sos_count > 0:
            return f"Game Over - {self.current_player_name} Wins!"


        if self.isGameOver():
            return "Game Over - It's a Draw!"

        
        return True


class GeneralSOS(SOSGame):
    def __init__(self, board_size):
        super().__init__(board_size)
        self.blue_score = 0
        self.red_score = 0

    def makeMove(self, row, column, letter):
        if not self.validateMove(row, column, letter):
            return False

        self.board[row][column] = letter

        
        sos_count = self.checkForSOS(row, column)

        
        if self.current_player_name == "Blue":
            self.blue_score += sos_count
        else:
            self.red_score += sos_count

        
        if self.isGameOver():
            if self.blue_score > self.red_score:
                return "Game Over - Blue Wins!"
            elif self.red_score > self.blue_score:
                return "Game Over - Red Wins!"
            else:
                return "Game Over - It's a Draw!"

        return True  


class Player(ABC):
    def __init__(self, name):
        self.name = name
        

    @abstractmethod
    def make_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def make_move(self, game):
        pass  # human move handled through GUI


class ComputerPlayer(Player):
    def __init__(self, name: str, letter: str):
        super().__init__(name)  
        self.letter = letter    

    def make_move(self, game):
        empty_cells = [
            (r, c)
            for r in range(game.board_size)
            for c in range(game.board_size)
            if game.getCell(r, c) == " "
        ]

        if not empty_cells:
            return

        row, col = random.choice(empty_cells)
        letter = random.choice(["S", "O"])
        self.letter = letter  
        game.board[row][col] = letter
