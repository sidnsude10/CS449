from src.sos_game import SimpleSOS, GeneralSOS
from src.sos_gui import SOSGUI
import tkinter as tk

def launchGame(board_size, game_mode):
    #Initializing and launching the SOS game GUI with the selected mode and board size
   
    game = SimpleSOS(board_size) if game_mode == 1 else GeneralSOS(board_size)

    #Set up GUI
    root = tk.Tk()
    root.title("SOS Game")  
    app = SOSGUI(root, game)
    root.mainloop()

def get_user_input(prompt, valid_range):
    """Handles user input validation"""
    while True:
        try:
            value = int(input(prompt))
            if value in valid_range:
                return value
            raise TypeError("Invalid mode selection. Must be 1 (Simple) or 2 (General).")
        except ValueError:
            print("Error: Please enter a valid number.")

if __name__ == "__main__":
    #Getting valid board size (must be at least 3)
    board_size = get_user_input("Enter board size (must be greater than 2): ", range(3, 100))

    #Getting valid game mode (1 = Simple, 2 = General)
    game_mode = get_user_input("Choose game mode (1 for Simple, 2 for General): ", {1, 2})

    #Starting game
    launchGame(board_size, game_mode)
