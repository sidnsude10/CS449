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
        self.switch_turn()
        return True  

    def switch_turn(self):
        self.current_turn = "O" if self.current_turn == "S" else "S"

    def checkForSOS(self, row=None, column=None):
        directions = [
            (0, 1), (1, 0), (1, 1), (-1, 1), 
            (0, -1), (-1, 0), (-1, -1), (1, -1)  
        ]

        found_sos = 0
        counted_positions = set()  

        if row is not None and column is not None:
            for dr, dc in directions:
                try:
                    sos_positions = {(row - dr, column - dc), (row, column), (row + dr, column + dc)}
                    if sos_positions.issubset(counted_positions):
                        continue  

                    if (
                        self.getCell(row - dr, column - dc) == "S"
                        and self.getCell(row, column) == "O"
                        and self.getCell(row + dr, column + dc) == "S"
                    ):
                        found_sos += 1
                        counted_positions.update(sos_positions)  

                    elif (
                        self.getCell(row, column) == "S"
                        and self.getCell(row - dr, column - dc) == "O"
                        and self.getCell(row + dr, column + dc) == "S"
                    ):
                        found_sos += 1
                        counted_positions.update(sos_positions)  

                except IndexError:
                    pass  

            return found_sos  

        for r in range(self.board_size):
            for c in range(self.board_size):
                for dr, dc in directions:
                    try:
                        if (
                            (self.getCell(r, c) == "O" and
                             self.getCell(r - dr, c - dc) == "S" and
                             self.getCell(r + dr, c + dc) == "S") 
                            or
                            (self.getCell(r, c) == "S" and
                             self.getCell(r - dr, c - dc) == "O" and
                             self.getCell(r + dr, c + dc) == "S") 
                        ):
                            found_sos += 1

                    except IndexError:
                        pass  

        return found_sos  

    def getGameState(self): 
        if isinstance(self, SimpleSOS):
            if self.isGameOver():  
                return "Game Over - It's a Draw!"

            for r in range(self.board_size):
                for c in range(self.board_size):
                    if self.checkForSOS(r, c) > 0:
                        winner = "Blue" if self.current_turn == "S" else "Red"
                        return f"Game Over - {winner} Wins!"  

            return "Game In Progress"

        if isinstance(self, GeneralSOS):
            if not self.isGameOver():
                return "Game In Progress"  

            blue_sos = self.sos_count["Blue"]
            red_sos = self.sos_count["Red"]

            if blue_sos > red_sos:
                return "Game Over - Blue Wins!"
            elif red_sos > blue_sos:
                return "Game Over - Red Wins!"

            return "Game Over - It's a Draw!"  

        return "Game In Progress"

    def isGameOver(self):
        return all(cell != " " for row in self.board for cell in row)


class SimpleSOS(SOSGame):
    def makeMove(self, row, column, letter):
        if not self.validateMove(row, column, letter):
            return False  

        self.board[row][column] = letter  
        last_player = "Blue" if self.current_turn == "S" else "Red"  

        sos_count = self.checkForSOS()
        if sos_count > 0:
            return f"Game Over - {last_player} Wins!"  

        if self.isGameOver():
            return "Game Over - It's a Draw!"

        self.switch_turn()
        return True  


class GeneralSOS(SOSGame):
    def __init__(self, board_size):
        super().__init__(board_size)
        self.sos_count = {"Blue": 0, "Red": 0}  

    def makeMove(self, row, column, letter):
        if not self.validateMove(row, column, letter):
            return False  

        self.board[row][column] = letter  
        player = "Blue" if self.current_turn == "S" else "Red"

        previous_sos_count = self.sos_count[player]  
        new_sos = self.checkForSOS(row, column)  

        if new_sos > 0 and new_sos != previous_sos_count:
            self.sos_count[player] += new_sos  

        if self.isGameOver():
            return self.getGameState()  

        self.switch_turn()
        return True  
