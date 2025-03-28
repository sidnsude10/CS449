import tkinter as tk
from src.sos_game import SimpleSOS, GeneralSOS

class SOSGUI:
    # graphical interface for the SOS game

    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.board_size = board.board_size
        self.cell_size = 50  # avoiding magic numbers
        self.game_mode = type(board)  # stores the original game mode
        self.current_turn_color = "blue"  # blue starts first
        self.selected_letter = tk.StringVar(value="S")  # tracks selected letter
        self.root.title("SOS Game")

        self.game_over = False  # tracks if the game has ended

        self.setup_ui()

    def setup_ui(self):
        # sets up the UI
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()

        # game mode selection
        self.game_mode_var = tk.IntVar(value=1)  # 1 for simple, 2 for general
        tk.Label(self.control_frame, text="SOS").pack(side="left")
        tk.Radiobutton(self.control_frame, text="Simple game", variable=self.game_mode_var, value=1).pack(side="left")
        tk.Radiobutton(self.control_frame, text="General game", variable=self.game_mode_var, value=2).pack(side="left")

        # board size input
        tk.Label(self.control_frame, text="Board size").pack(side="left")
        self.board_size_entry = tk.Entry(self.control_frame, width=5)
        self.board_size_entry.pack(side="left")
        self.board_size_entry.insert(0, str(self.board_size))  # default to current size

        # game board frame
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.create_board()

        # turn indicator
        self.turn_label = tk.Label(self.root, text="Current turn: Blue", fg="blue")
        self.turn_label.pack()

        # letter selection
        self.letter_frame = tk.Frame(self.root)
        self.letter_frame.pack()
        tk.Label(self.letter_frame, text="Pick a letter:").pack(side="left")
        tk.Radiobutton(self.letter_frame, text="S", variable=self.selected_letter, value="S").pack(side="left")
        tk.Radiobutton(self.letter_frame, text="O", variable=self.selected_letter, value="O").pack(side="left")

        # game over display
        self.game_over_label = tk.Label(self.root, text="", fg="red", font=("Arial", 12, "bold"))
        self.game_over_label.pack()

        # reset button
        self.reset_button = tk.Button(self.root, text="New Game", command=self.restart_game)
        self.reset_button.pack(pady=10)

    def restart_game(self):
        # resets the game while keeping the same mode and board size
        try:
            new_size = int(self.board_size_entry.get())
            if new_size < 3:
                raise ValueError
        except ValueError:
            self.board_size_entry.delete(0, tk.END)
            self.board_size_entry.insert(0, str(self.board_size))
            return

        self.board_size = new_size
        game_mode_class = SimpleSOS if self.game_mode_var.get() == 1 else GeneralSOS
        self.board = game_mode_class(self.board_size)

        self.create_board()
        self.update_board_display()

        self.turn_label.config(text="Current turn: Blue", fg="blue")
        self.current_turn_color = "blue"

        self.game_over_label.config(text="")
        self.game_over = False  # resets game state

        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board_buttons[r][c]:  
                    self.board_buttons[r][c].config(state=tk.NORMAL)

    def create_board(self):
        # clears the old board before making a new one
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.board_buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        for r in range(self.board_size):
            for c in range(self.board_size):
                btn = tk.Button(self.board_frame, text=" ", width=4, height=2,
                                command=lambda row=r, col=c: self.handle_move(row, col))
                btn.grid(row=r, column=c, padx=2, pady=2)

                self.board_buttons[r][c] = btn  # store button reference

    def handle_move(self, row, col):
        # handles player moves and updates the GUI
        if self.game_over:  
            return  # stops moves after game over

        letter = self.selected_letter.get()
        move_result = self.board.makeMove(row, col, letter)

        if isinstance(move_result, str) and move_result.startswith("Game Over"):
            self.game_over_label.config(text=move_result)

            # disables board so no more moves can be made
            self.disable_board()

            # sets game_over flag to stop future moves
            self.game_over = True
        else:
            self.update_board_display()
        
            # updates turn label after a move
            current_player = "Blue" if self.board.current_turn == "S" else "Red"
            self.turn_label.config(text=f"Turn: {current_player}", fg="blue" if current_player == "Blue" else "red")

    def update_board_display(self):
        # updates the board UI
        if not self.board_buttons:
            return

        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board_buttons[r][c]:
                    cell_value = self.board.getCell(r, c)
                    self.board_buttons[r][c].config(text=cell_value if cell_value in ("S", "O") else " ")

    def disable_board(self):
        # disables all board buttons after game over
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board_buttons[r][c]:
                    self.board_buttons[r][c].config(state=tk.DISABLED)

    def switch_turn(self):
        # switches the turn between blue and red
        if self.current_turn_color == "blue":
            self.current_turn_color = "red"
            self.turn_label.config(text="Current turn: Red", fg="red")
        else:
            self.current_turn_color = "blue"
            self.turn_label.config(text="Current turn: Blue", fg="blue")

if __name__ == "__main__":
    root = tk.Tk()
    game = SimpleSOS(3)
    app = SOSGUI(root, game)
    root.mainloop()
