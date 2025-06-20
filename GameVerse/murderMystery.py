import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to start the game with selected difficulty
def start_level_1(level):
    global difficulty
    difficulty = level # Store selected difficulty level
    root.destroy()  # Close the dashboard
    import MMLevel1 # Load the game script
def start_level_2(level):
    global difficulty
    difficulty = level # Store selected difficulty level
    root.destroy()  # Close the dashboard
    import MMLevel2
def start_level_3(level):
    global difficulty
    difficulty = level # Store selected difficulty level
    root.destroy()  # Close the dashboard
    import MMLevel3

def back(home):
    root.destroy()
    #os.system(f"python Home.py")
# Create main dashboard window
root = tk.Tk()
root.title("Game Dashboard")
root.geometry("500x400")
root.configure(bg="#2C2F33")
root.resizable(False, False)

# Load and display background image
bg_image = Image.open("C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/murderMysteryassets/bg.jpeg")
bg_image = bg_image.resize((500, 400))
bg_photo = ImageTk.PhotoImage(bg_image)
label_bg = tk.Label(root, image=bg_photo)
label_bg.place(relwidth=1, relheight=1)

# Title Label
title_label = tk.Label(root, text="Select Game Difficulty", font=("Helvetica", 18, "bold"), fg="white", bg="#23272A")
title_label.pack(pady=20)

# Buttons for different levels
btn_easy = tk.Button(root, text="Easy", command=lambda: start_level_1("MMLevel1"), font=("Arial", 14, "bold"), bg="#28a745", fg="white", width=15)
btn_easy.pack(pady=10)

btn_medium = tk.Button(root, text="Medium", command=lambda: start_level_2("MMLevel2"), font=("Arial", 14, "bold"), bg="#ffc107", fg="black", width=15)
btn_medium.pack(pady=10)

btn_hard = tk.Button(root, text="Hard", command=lambda: start_level_3("MMLevel3"), font=("Arial", 14, "bold"), bg="#dc3545", fg="white", width=15)
btn_hard.pack(pady=10)

back_button = tk.Button(root, text="BACK", command=lambda: back("Home.py"), font=("Arial", 14, "bold"), bg="#99AAB5", fg="black")
back_button.pack(side=tk.RIGHT, padx=10)
# Run the dashboard
root.mainloop()