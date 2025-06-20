import sqlite3
import random
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk  # Importing Pillow for image handling
import os
# Set up SQLite database (persistent)
conn = sqlite3.connect("murder_mystery.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS suspects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS weapons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    suspect_id INTEGER,
    weapon_id INTEGER,
    location_id INTEGER,
    clue TEXT,
    FOREIGN KEY(suspect_id) REFERENCES suspects(id),
    FOREIGN KEY(weapon_id) REFERENCES weapons(id),
    FOREIGN KEY(location_id) REFERENCES locations(id)
)
""")
cursor.execute("DELETE FROM suspects")
cursor.execute("DELETE FROM weapons")
cursor.execute("DELETE FROM locations")
cursor.execute("DELETE FROM evidence")

# Reset auto-increment counter for all tables
cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('suspects', 'weapons', 'locations', 'evidence')")

conn.commit()
# Game data
suspects = ["Alice", "Bob", "Charlie", "Diana"]
weapons = ["Knife", "Gun", "Poison", "Baseball Bat"]
locations = ["Library", "Kitchen", "Garden", "Study"]

# Insert data into tables if not already present
for suspect in suspects:
    cursor.execute("INSERT OR IGNORE INTO suspects (name) VALUES (?)", (suspect,))
for weapon in weapons:
    cursor.execute("INSERT OR IGNORE INTO weapons (name) VALUES (?)", (weapon,))
for location in locations:
    cursor.execute("INSERT OR IGNORE INTO locations (name) VALUES (?)", (location,))

conn.commit()

# Generate solution only if it's not already in evidence
cursor.execute("SELECT COUNT(*) FROM evidence")
if cursor.fetchone()[0] == 0:
    culprit = random.choice(suspects)
    murder_weapon = random.choice(weapons)
    crime_location = random.choice(locations)

    clues = [
        f"The culprit was seen near the {crime_location}.",
        f"The murder weapon might be a {murder_weapon}.",
        f"Someone mentioned {culprit} acting suspiciously."
    ]

    cursor.execute("""
    INSERT INTO evidence (suspect_id, weapon_id, location_id, clue)
    VALUES (
        (SELECT id FROM suspects WHERE name = ?),
        (SELECT id FROM weapons WHERE name = ?),
        (SELECT id FROM locations WHERE name = ?),
        ?
    )
    """, (culprit, murder_weapon, crime_location, random.choice(clues)))
    conn.commit()
else:
    cursor.execute("""
    SELECT suspects.name, weapons.name, locations.name FROM evidence
    JOIN suspects ON evidence.suspect_id = suspects.id
    JOIN weapons ON evidence.weapon_id = weapons.id
    JOIN locations ON evidence.location_id = locations.id
    """)
    culprit, murder_weapon, crime_location = cursor.fetchone()

# Custom message box
class CustomMessagebox(tk.Toplevel):
    def __init__(self, title, message, color):
        super().__init__()
        self.title(title)
        self.geometry("400x200")
        self.configure(bg=color)

        self.bg_image = Image.open("C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/murderMysteryassets/bg.jpeg")
        self.bg_image = self.bg_image.resize((400, 200))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        label_bg = tk.Label(self, image=self.bg_photo)
        label_bg.place(relwidth=1, relheight=1)

        label = tk.Label(self, text=message, font=("Arial", 12, "bold"), fg="white", bg=color, wraplength=350)
        label.pack(pady=30)

        ok_button = ttk.Button(self, text="OK", command=self.destroy)
        ok_button.pack()

def show_message(title, message, color="#7289DA"):
    CustomMessagebox(title, message, color)

# Custom simple dialog
class CustomSimpleDialog(tk.Toplevel):
    def __init__(self, title, prompt):
        super().__init__()
        self.title(title)
        self.geometry("350x180")
        self.configure(bg="#7289DA")

        self.bg_image = Image.open("C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/murderMysteryassets/bg.jpeg")
        self.bg_image = self.bg_image.resize((350, 180))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        label_bg = tk.Label(self, image=self.bg_photo)
        label_bg.place(relwidth=1, relheight=1)

        label = tk.Label(self, text=prompt, font=("Arial", 12, "bold"), fg="white", bg="#2C2F33")
        label.pack(pady=20)

        self.entry = tk.Entry(self, font=("Arial", 12))
        self.entry.pack(pady=5)

        button_frame = tk.Frame(self, bg="#2C2F33")
        button_frame.pack(pady=10)

        submit_button = ttk.Button(button_frame, text="Submit", command=self.submit)
        submit_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        self.result = None
        self.wait_window()
    def submit(self):
        self.result = self.entry.get()
        self.destroy()

def custom_askstring(title, prompt):
    dialog = CustomSimpleDialog(title, prompt)
    return dialog.result

# Tkinter UI
def execute_query():
    query = query_entry.get().strip()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        output_box.delete("1.0", tk.END)
        for row in results:
            output_box.insert(tk.END, str(row) + "\n")
        conn.commit()
    except Exception as e:
        show_message("Query Error", f"Error in query: {e}", "#E74C3C")

def solve_mystery():
    suspect_guess = custom_askstring("Solve Mystery", "Who is the culprit?")
    weapon_guess = custom_askstring("Solve Mystery", "What is the murder weapon?")
    location_guess = custom_askstring("Solve Mystery", "Where did the murder happen?")

    if (suspect_guess and weapon_guess and location_guess and
        suspect_guess.lower() == culprit.lower() and
        weapon_guess.lower() == murder_weapon.lower() and
        location_guess.lower() == crime_location.lower()):
        show_message("Congratulations!", f"You solved the mystery! The culprit was {culprit}, using the {murder_weapon} in the {crime_location}.", "#2ECC71")
    else:
        show_message("Wrong Guess", "Incorrect guess. Keep investigating!", "#E74C3C")

def back(backhome):
    #global difficulty
    #difficulty = backhome # Store selected difficulty level
    root.destroy()  # Close the dashboard
    os.system(f"python murderMystery.py")
def show_table():
    show_message("Availabe Table ","EVIDENCE : which helps to get clues.\nSUSPECTS : which shows people involved in murder.\nWEAPONS : which conatins weapons found at crime location.\n LOCATIONS : which contains the locations where the clues where found.", "#2C2F33")
def hints():
    show_message("HINT","Select * From Evidence;\n\n apply this query to all tables.","#2C2F33")
root = tk.Tk()
root.title("SQL Murder Mystery Game")
root.geometry("600x500")
root.configure(bg="#2C2F33")
root.resizable(False, False)

bg_image = Image.open("C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/murderMysteryassets/bg.jpeg")
bg_image = bg_image.resize((600, 500))
bg_photo = ImageTk.PhotoImage(bg_image)

label_bg = tk.Label(root, image=bg_photo)
label_bg.place(relwidth=1, relheight=1)

# Title Label
title_label = tk.Label(root, text="SQL Murder Mystery LEVEL 1", font=("Helvetica", 18, "bold"), fg="white", bg="#23272A")
title_label.pack(pady=10, fill=tk.X)
hint_button = tk.Button(root, text="Hint", command=hints, font=("Arial", 12, "bold"), bg="#99AAB5", fg="black")
hint_button.place(relx=0.9, rely=0.02, anchor="ne")  # Positioned in the top-right corner
# Query Entry
query_frame = tk.Frame(root, bg="#2C2F33",bd=5)
query_frame.pack(pady=20)
query_label = tk.Label(query_frame, text="Enter SQL Query:", font=("Arial", 12), fg="white", bg="#2C2F33")
query_label.pack()
query_entry = tk.Entry(query_frame, width=50, font=("Arial", 12))
query_entry.pack(pady=5)

# Query Execution Button
execute_button = tk.Button(query_frame, text="Execute Query", command=execute_query, font=("Arial", 12), bg="#99AAB5", fg="black")
execute_button.pack(pady=5)
execute_button = tk.Button(query_frame, text="Availabe tables", command=show_table, font=("Arial", 12), bg="#99AAB5", fg="black")
execute_button.pack(pady=5)


# Output Box
output_box = scrolledtext.ScrolledText(root, width=70, height=10, font=("Courier", 10), bg="#2C2F33",fg="white",bd=1)
output_box.pack(pady=10)

# Frame to align Solve Mystery and Back buttons
button_frame = tk.Frame(root, bg="#2C2F33")
button_frame.pack(pady=10)

# Solve Mystery Button (left side)
solve_button = tk.Button(button_frame, text="Solve the Mystery", command=solve_mystery, font=("Arial", 14, "bold"), bg="#99AAB5", fg="black")
solve_button.pack(side=tk.LEFT, padx=10)

# Back Button (right side)
back_button = tk.Button(button_frame, text="BACK", command=lambda: back("murderMystery"), font=("Arial", 14, "bold"), bg="#99AAB5", fg="black")
back_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()