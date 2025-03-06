class SOSGame:
    #Base class for SOS game logic
    def __init__(self, board_size):
        if board_size < 3:
            raise ValueError("Board size must be at least 3x3.")
        
        self.board_size = board_size
        self.board = [[" " for _ in range(board_size)] for _ in range(board_size)]
        self.current_turn = "S"  #S starts

    def getCell(self, row, column):
        #Return the value of a specific cell or None if value is out of bounds
        if 0 <= row < self.board_size and 0 <= column < self.board_size:
            return self.board[row][column]
        return None  

    def makeMove(self, row, column, letter):
        #Handles placing moves. Child classes will inheret when needed
        if not (0 <= row < self.board_size and 0 <= column < self.board_size):
            return False  
        if self.board[row][column] != " " or letter not in ("S", "O"):
            return False  
        
        self.board[row][column] = letter  
        self.switch_turn()  
        return True

    def switch_turn(self):
        self.current_turn = "O" if self.current_turn == "S" else "S"


class SimpleSOS(SOSGame):
    def makeMove(self, row, column, letter):
        return super().makeMove(row, column, letter)


class GeneralSOS(SOSGame):
    def makeMove(self, row, column, letter):
        return super().makeMove(row, column, letter)  
