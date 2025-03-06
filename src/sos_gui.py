import tkinter as tk
from src.sos_game import SOSGame, SimpleSOS, GeneralSOS

class SOSGUI:
    #graphical interface for the SOS game

    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.board_size = board.board_size
        self.cell_size = 50  # avoiding magic numbers
        self.game_mode = type(board)  # stores the original game mode
        self.selected_letter = tk.StringVar(value="S")  # will tracks selected letter
        self.root.title("SOS Game")
        self.setup_ui()

    def setup_ui(self):
        #UI layout
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.board_buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for r in range(self.board_size):
            for c in range(self.board_size):
                btn = tk.Button(self.board_frame, text=" ", width=4, height=2, 
                                command=lambda row=r, col=c: self.handle_move(row, col))
                btn.grid(row=r, column=c, ipadx=self.cell_size // 4, ipady=self.cell_size // 6)
                self.board_buttons[r][c] = btn

        self.turn_label = tk.Label(self.root, text=f"Turn: {self.board.current_turn}")
        self.turn_label.pack()
        self.letter_frame = tk.Frame(self.root)
        self.letter_frame.pack()
        tk.Label(self.letter_frame, text="Pick a letter:").pack(side="left")
        tk.Radiobutton(self.letter_frame, text="S", variable=self.selected_letter, value="S").pack(side="left")
        tk.Radiobutton(self.letter_frame, text="O", variable=self.selected_letter, value="O").pack(side="left")
        self.reset_button = tk.Button(self.root, text="New Game", command=self.restart_game)
        self.reset_button.pack(pady=10)

    def handle_move(self, row, col):
        #get the players move and update the GUI
        letter = self.selected_letter.get()  # Get the letter chosen by the player
        move_made = self.board.makeMove(row, col, letter)
        if move_made:  
            self.update_board_display()
            self.turn_label.config(text=f"Turn: {self.board.current_turn}")

    def update_board_display(self):
        #update board
        for r in range(self.board_size):
            for c in range(self.board_size):
                cell_value = self.board.getCell(r, c)
                if cell_value in ("S", "O"):
                    self.board_buttons[r][c].config(text=cell_value)
                else:
                    self.board_buttons[r][c].config(text=" ")

    def restart_game(self):
        #reseting the game but  still keeps the settings
        self.board = self.game_mode(self.board_size)  # keep original mode
        self.update_board_display()
        self.turn_label.config(text=f"Turn: {self.board.current_turn}")

if __name__ == "__main__":
    root = tk.Tk()
    game = SimpleSOS(3)  # default board size will be 3x3 & start in simple mode
    app = SOSGUI(root, game)
    root.mainloop()
