import tkinter as tk
from tkinter import messagebox

def on_check():
    messagebox.showinfo("Checkbox", "Checkbox clicked!")

def on_radio():
    selected = radio_var.get()
    messagebox.showinfo("Radio Button", f"Selected Option: {selected}")

def on_click(row, col):
    if board[row][col]["text"] == "":
        board[row][col]["text"] = "S" if turn.get() == "Blue" else "O"
        toggle_turn()

def toggle_turn():
    turn.set("Red" if turn.get() == "Blue" else "Blue")

# Initializing
root = tk.Tk()
root.title("SOS Game GUI")
root.geometry("400x400")

# title label
label = tk.Label(root, text="SOS Game", font=("Arial", 16))
label.pack(pady=10)

# Create gameboard
frame = tk.Frame(root)
frame.pack()
board = []
turn = tk.StringVar(value="Blue")
for r in range(3):
    row = []
    for c in range(3):
        btn = tk.Button(frame, text="", width=5, height=2, command=lambda r=r, c=c: on_click(r, c))
        btn.grid(row=r, column=c)
        row.append(btn)
    board.append(row)

# checkbox
check_button = tk.Checkbutton(root, text="Enable Special Mode", command=on_check)
check_button.pack()

# radio buttons
radio_var = tk.StringVar(value="PvP")
radio1 = tk.Radiobutton(root, text="Player vs Player", variable=radio_var, value="PvP", command=on_radio)
radio2 = tk.Radiobutton(root, text="Player vs Computer", variable=radio_var, value="PvC", command=on_radio)
radio1.pack()
radio2.pack()

# Run Tkinter event loop
root.mainloop()