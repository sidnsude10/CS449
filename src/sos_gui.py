import tkinter as tk
import random
from src.sos_game import SimpleSOS, GeneralSOS
from src.sos_game import HumanPlayer, ComputerPlayer


class SOSGUI:

    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.board_size = board.board_size
        self.cell_size = 50  # avoiding magic numbers
        self.game_mode = type(board)  
        self.current_turn_color = "blue"  # blue starts first
        self.root.title("SOS Game")

        self.game_over = False  
        self.current_player = None 


        self.setup_ui()

    def setup_ui(self):
        # sets up the UI
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()

        # game mode selection
        self.game_mode_var = tk.IntVar(value=1)  
        tk.Label(self.control_frame, text="SOS").pack(side="left")
        tk.Radiobutton(self.control_frame, text="Simple game", variable=self.game_mode_var, value=1).pack(side="left")
        tk.Radiobutton(self.control_frame, text="General game", variable=self.game_mode_var, value=2).pack(side="left")

        # board size input
        tk.Label(self.control_frame, text="Board size").pack(side="left")
        self.board_size_entry = tk.Entry(self.control_frame, width=5)
        self.board_size_entry.pack(side="left")
        self.board_size_entry.insert(0, str(self.board_size))  

        # Blue Player
        self.blue_player_frame = tk.Frame(self.root)
        self.blue_player_frame.pack(side="left", padx=20)

        tk.Label(self.blue_player_frame, text="Blue player").pack()
        self.blue_type = tk.StringVar(value="human")
        tk.Radiobutton(self.blue_player_frame, text="Human", variable=self.blue_type, value="human").pack()
        tk.Radiobutton(self.blue_player_frame, text="Computer", variable=self.blue_type, value="computer").pack()

        # Red Player 
        self.red_player_frame = tk.Frame(self.root)
        self.red_player_frame.pack(side="right", padx=20)

        tk.Label(self.red_player_frame, text="Red player").pack()
        self.red_type = tk.StringVar(value="human")
        tk.Radiobutton(self.red_player_frame, text="Human", variable=self.red_type, value="human").pack()
        tk.Radiobutton(self.red_player_frame, text="Computer", variable=self.red_type, value="computer").pack()

        # letter selection for human players
        self.selected_letter = tk.StringVar(value="S")
        self.letter_frame = tk.Frame(self.root)
        self.letter_frame.pack()
        tk.Label(self.letter_frame, text="Pick a letter:").pack(side="left")
        tk.Radiobutton(self.letter_frame, text="S", variable=self.selected_letter, value="S").pack(side="left")
        tk.Radiobutton(self.letter_frame, text="O", variable=self.selected_letter, value="O").pack(side="left")

        # game board frame
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.create_board()

        # turn indicator
        self.turn_label = tk.Label(self.root, text="Current turn: Blue", fg="blue")
        self.turn_label.pack()

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

               # Create Blue Player
        if self.blue_type.get() == "human":
            from src.sos_game import HumanPlayer
            self.blue_player = HumanPlayer("Blue")
        else:
            from src.sos_game import ComputerPlayer
            self.blue_player = ComputerPlayer("Blue", random.choice(["S", "O"]))

        # Create Red Player
        if self.red_type.get() == "human":
            from src.sos_game import HumanPlayer
            self.red_player = HumanPlayer("Red")
        else:
            from src.sos_game import ComputerPlayer
            self.red_player = ComputerPlayer("Red", random.choice(["S", "O"]))


        # Start with blue
        self.current_player = self.blue_player

        self.create_board()
        self.update_board_display()

        self.turn_label.config(text="Current turn: Blue", fg="blue")
        self.current_turn_color = "blue"

        self.game_over_label.config(text="")
        self.game_over = False  

        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board_buttons[r][c]:
                    self.board_buttons[r][c].config(state=tk.NORMAL)

        if isinstance(self.current_player, ComputerPlayer):
            self.root.after(500, self.computer_move)


    def create_board(self):
        # clears old board before making a new one
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.board_buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        for r in range(self.board_size):
            for c in range(self.board_size):
                btn = tk.Button(self.board_frame, text=" ", width=4, height=2,
                                command=lambda row=r, col=c: self.handle_move(row, col))
                btn.grid(row=r, column=c, padx=2, pady=2)

                self.board_buttons[r][c] = btn  

    def handle_move(self, row, col):
        if self.game_over:
            return

        
        if not self.current_player:
            return

        
        if isinstance(self.current_player, HumanPlayer):
            letter = self.selected_letter.get()
        elif isinstance(self.current_player, ComputerPlayer):
            letter = self.current_player.letter
        else:
            return

        
        self.board.current_player_name = self.current_player.name
        move_result = self.board.makeMove(row, col, letter)

        if isinstance(move_result, str) and move_result.startswith("Game Over"):
            self.update_board_display()

            # Only end game immediately in Simple mode
            if isinstance(self.board, SimpleSOS):
                self.game_over_label.config(text=move_result)
                self.disable_board()
                self.game_over = True
                return

            # In General mode, only end if the board is full
            elif isinstance(self.board, GeneralSOS) and self.board.isGameOver():
                self.game_over_label.config(text=move_result)
                self.disable_board()
                self.game_over = True
                return

        
        self.update_board_display()
        self.switch_turn()

        
        if isinstance(self.current_player, ComputerPlayer):
            self.root.after(500, self.computer_move)




    def computer_move(self):
        if self.game_over or not isinstance(self.current_player, ComputerPlayer):
            return

        # Tell the game logic who the current player is
        self.board.current_player_name = self.current_player.name

        self.current_player.make_move(self.board)
        self.update_board_display()

        if self.board.isGameOver() or "Game Over" in self.board.getGameState():
            self.game_over_label.config(text=self.board.getGameState())
            self.disable_board()
            self.game_over = True
            return

        self.switch_turn()

        if isinstance(self.current_player, ComputerPlayer):
            self.root.after(500, self.computer_move)


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
        if self.current_player == self.blue_player:
            self.current_player = self.red_player
            self.turn_label.config(text="Current turn: Red", fg="red")
        else:
            self.current_player = self.blue_player
            self.turn_label.config(text="Current turn: Blue", fg="blue")


if __name__ == "__main__":
    root = tk.Tk()
    game = SimpleSOS(3)
    app = SOSGUI(root, game)
    root.mainloop()
