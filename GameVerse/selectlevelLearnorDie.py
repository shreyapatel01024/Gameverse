import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import sys
import subprocess

# Database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2424",
        database="gameverse"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to database: {err}")
    sys.exit()

# Get the logged-in user ID from command line arguments
logged_in_userid = sys.argv[1] if len(sys.argv) > 1 else ""

def launch_level(level_number, user_id):
    print(f"Launching Level {level_number} for User {user_id}")
    try:
        subprocess.Popen(
            [sys.executable, f"LearnorDieL{level_number}.py", str(user_id)],
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch 'Learn or Die': {e}")

    messagebox.showinfo("Hello","Just testing")



levels_win = tk.Tk()
levels_win.title("Learn or Die - Select Level")
levels_win.geometry("400x400")

tk.Label(levels_win, text="Select Level", font=("Arial", 18, "bold")).pack(pady=10)

# Get game_id for 'Learn Or Die'
cursor.execute("SELECT game_id FROM games WHERE name = 'Learn Or Die'")
game = cursor.fetchone()

if not game:
    messagebox.showerror("Error", "Learn Or Die game entry not found!")
    levels_win.destroy()
else:
    game_id = game[0]

    # Get the highest level the user has reached
    cursor.execute("SELECT level FROM scores WHERE user_id=%s AND game_id=%s", (logged_in_userid, game_id))
    level = cursor.fetchone()

    max_level = level[0] if level else 1

    tk.Label(levels_win, text=f"Current Level: {max_level}", font=("Arial", 14)).pack(pady=5)

    # Create buttons for each level
    for lvl in range(1, max_level + 1):
        tk.Button(levels_win, text=f"Level {lvl}", font=("Arial", 14), width=15,
                  command=lambda l=lvl: launch_level(l, logged_in_userid)).pack(pady=5)

    tk.Button(levels_win, text="Close", command=levels_win.destroy).pack(pady=10)

levels_win.mainloop()
