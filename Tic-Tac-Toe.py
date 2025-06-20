import tkinter as tk
import random
import mysql.connector
from PIL import Image, ImageTk
import sys
# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2424",
        database="gameverse"
    )
gameid=1
# Fetch the highest score from the database
if len(sys.argv) > 1:
    logged_in_username = sys.argv[1]
else:
    logged_in_username = ""
con=connect_db()
cursor1=con.cursor()
cursor1.execute(f"Select * from users where username='{logged_in_username}'")
userid=cursor1.fetchone()
def get_highest_score():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT score FROM scores where user_id={userid[0]} and game_id={gameid}")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

# Update the highest score in the database
def update_highest_score(new_score):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE scores SET score ={score} WHERE user_id ={userid[0]} and game_id={gameid}")
    conn.commit()
    conn.close()

# Check if a player has won
def check_winner(board, symbol):
    for row in board:
        if all(cell == symbol for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == symbol for row in range(3)):
            return True
    if all(board[i][i] == symbol for i in range(3)) or all(board[i][2 - i] == symbol for i in range(3)):
        return True
    return False

# Check for a draw
def is_draw(board):
    return all(cell != "" for row in board for cell in row)

# Minimax algorithm for AI
def minimax(board, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = "O"
                    score = minimax(board, False)
                    board[r][c] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = "X"
                    score = minimax(board, True)
                    board[r][c] = ""
                    best_score = min(score, best_score)
        return best_score

# AI best move logic
def best_move():
    result_label.config(text="Computer's Turn")
    root.update_idletasks()

    move = None
    difficulty = random.random()

    if difficulty < 0.3:
        best_score = -float("inf")
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = "O"
                    score = minimax(board, False)
                    board[r][c] = ""
                    if score > best_score:
                        best_score = score
                        move = (r, c)
    else:
        available_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
        move = random.choice(available_moves) if available_moves else None

    if move:
        row, col = move
        board[row][col] = "O"
        buttons[row][col].config(image=o_img, state=tk.DISABLED)

        if check_winner(board, "O"):
            result_label.config(text="Computer Wins!")
            disable_all_buttons()
        elif is_draw(board):
            result_label.config(text="It's a Draw!")
        else:
            result_label.config(text="Your Turn")

# Handle player's move
def player_move(row, col):
    global score
    if board[row][col] == "":
        board[row][col] = "X"
        buttons[row][col].config(image=x_img, state=tk.DISABLED)

        if check_winner(board, "X"):
            result_label.config(text="You Win!")
            disable_all_buttons()
            score += 1
            score_label.config(text=f"Score: {score}")

            if score > highest_score:
                update_highest_score(score)
                highest_score_label.config(text=f"Highest Score: {score}")

        elif is_draw(board):
            result_label.config(text="It's a Draw!")
        else:
            root.after(500, best_move)

# Disable all buttons
def disable_all_buttons():
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(state=tk.DISABLED)

# Reset the game
def reset_game():
    global board, score, highest_score
    board = [["" for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(image=empty_img, state=tk.NORMAL)
    result_label.config(text="Your Turn")

    score_label.config(text=f"Score:{score}")

    highest_score = get_highest_score()
    highest_score_label.config(text=f"Highest Score: {highest_score}")
    if score > highest_score:
        update_highest_score(score)
        highest_score_label.config(text=f"Highest Score: {score}")

# Initialize main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_size = min(screen_width, screen_height) // 2
button_size = window_size // 3

root.geometry(f"{window_size}x{window_size + 150}")


board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
score = 0
highest_score = get_highest_score()

# Load images
empty_img = ImageTk.PhotoImage(Image.new('RGB', (button_size, button_size), (255, 255, 255)))
x_img = ImageTk.PhotoImage(Image.open("C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/X.jpeg").resize((button_size, button_size)))
o_img = ImageTk.PhotoImage(Image.open("C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/O.jpeg").resize((button_size, button_size)))

frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

for r in range(3):
    for c in range(3):
        buttons[r][c] = tk.Button(frame, image=empty_img, height=button_size, width=button_size, command=lambda r=r, c=c: player_move(r, c))
        buttons[r][c].grid(row=r, column=c, sticky="nsew")

result_label = tk.Label(root, text="Your Turn", font=("Arial", 16))
result_label.pack(fill="x", padx=10, pady=5)

score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 14))
score_label.pack(fill="x", padx=10)

highest_score_label = tk.Label(root, text=f"Highest Score: {highest_score}", font=("Arial", 14))
highest_score_label.pack(fill="x", padx=10)

restart_button = tk.Button(root, text="Restart", font=("Arial", 14), command=reset_game)
restart_button.pack(fill="x", padx=10, pady=5)

root.mainloop()
