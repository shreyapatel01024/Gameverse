import sqlite3
import random
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk

# Persistent SQLite database
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
# Check if 'type' column exists in 'evidence'
cursor.execute("PRAGMA table_info(evidence)")
columns = [col[1] for col in cursor.fetchall()]
if "type" not in columns:
    print("Updating database schema: Adding 'type' column to 'evidence' table.")

    # Rename old table
    cursor.execute("ALTER TABLE evidence RENAME TO old_evidence")

    # Create new evidence table with 'type' column
    cursor.execute("""
    CREATE TABLE evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        suspect_id INTEGER,
        weapon_id INTEGER,
        location_id INTEGER,
        clue TEXT,
        type TEXT,  -- Added column
        FOREIGN KEY(suspect_id) REFERENCES suspects(id),
        FOREIGN KEY(weapon_id) REFERENCES weapons(id),
        FOREIGN KEY(location_id) REFERENCES locations(id)
    )
    """)

    # Migrate old data (type will be 'true' by default for existing records)
    cursor.execute("""
    INSERT INTO evidence (id, suspect_id, weapon_id, location_id, clue, type)
    SELECT id, suspect_id, weapon_id, location_id, clue, 'true' FROM old_evidence
    """)

    # Drop old table
    cursor.execute("DROP TABLE old_evidence")
    conn.commit()

# Reset tables and ensure fresh start
cursor.execute("DELETE FROM suspects")
cursor.execute("DELETE FROM weapons")
cursor.execute("DELETE FROM locations")
cursor.execute("DELETE FROM evidence")

# Reset the auto-increment counter
cursor.execute("DELETE FROM sqlite_sequence WHERE name='suspects'")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='weapons'")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='locations'")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='evidence'")

conn.commit()

# Extended game data for added difficulty
suspects = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]
weapons = ["Knife", "Gun", "Poison", "Baseball Bat", "Rope", "Hammer", "Dagger", "Axe"]
locations = ["Library", "Kitchen", "Garden", "Study", "Garage", "Basement", "Rooftop", "Dining Room"]

# Insert data only if tables are empty
cursor.execute("SELECT COUNT(*) FROM suspects")
if cursor.fetchone()[0] == 0:
    for suspect in suspects:
        cursor.execute("INSERT INTO suspects (name) VALUES (?)", (suspect,))

cursor.execute("SELECT COUNT(*) FROM weapons")
if cursor.fetchone()[0] == 0:
    for weapon in weapons:
        cursor.execute("INSERT INTO weapons (name) VALUES (?)", (weapon,))

cursor.execute("SELECT COUNT(*) FROM locations")
if cursor.fetchone()[0] == 0:
    for location in locations:
        cursor.execute("INSERT INTO locations (name) VALUES (?)", (location,))

conn.commit()
# Generate solution
culprit = random.choice(suspects)
murder_weapon = random.choice(weapons)
crime_location = random.choice(locations)

# *Limited guesses*
# Number of attempts before evidence changes
MAX_ATTEMPTS = 3
attempts_left = MAX_ATTEMPTS

# Clear old evidence before inserting new clues
cursor.execute("DELETE FROM evidence")
conn.commit()

# Generate multiple pieces of evidence
true_clues = [
    f"The culprit was seen near the {crime_location}.",
    f"The murder weapon might be a {murder_weapon}.",
    f"Someone mentioned {culprit} acting suspiciously."
]

# Generate false/misleading clues
false_clues = [
    f"People suspect {random.choice(suspects)}.",
    f"A {random.choice(weapons)} was found, but it's unclear if it's the murder weapon.",
    f"A witness claims the murder happened in the {random.choice(locations)}."
]

# Shuffle clues and insert into database
all_clues = true_clues + random.sample(false_clues, 2)  # Mix true and false clues

for clue in all_clues:
    clue_type = "true" if clue in true_clues else "false"
    cursor.execute("""
    INSERT INTO evidence (suspect_id, weapon_id, location_id, clue, type)
    VALUES (
        (SELECT id FROM suspects WHERE name = ?),
        (SELECT id FROM weapons WHERE name = ?),
        (SELECT id FROM locations WHERE name = ?),
        ?, ?
        )
    """, (culprit, murder_weapon, crime_location, clue, clue_type))
conn.commit()


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
    global attempts_left

    if attempts_left <= 0:
        reset_evidence()
        attempts_left = MAX_ATTEMPTS
        show_message("New Evidence", "All your attempts are over! The evidence has changed.", "#E74C3C")
        return

    suspect_guess = custom_askstring("Solve Mystery", "Who is the culprit?")
    weapon_guess = custom_askstring("Solve Mystery", "What is the murder weapon?")
    location_guess = custom_askstring("Solve Mystery", "Where did the murder happen?")

    if (suspect_guess and weapon_guess and location_guess and
            suspect_guess.lower() == culprit.lower() and
            weapon_guess.lower() == murder_weapon.lower() and
            location_guess.lower() == crime_location.lower()):
        show_message("Congratulations!",
                     f"You solved the mystery! The culprit was {culprit}, using the {murder_weapon} in the {crime_location}.",
                     "#2ECC71")
    else:
        attempts_left -= 1
        if attempts_left > 0:
            show_message("Wrong Guess", f"Incorrect guess. Attempts left: {attempts_left}", "#E74C3C")
        else:
            reset_evidence()
            show_message("Game Over", "All attempts are over! The evidence has changed.", "#E74C3C")
            attempts_left = MAX_ATTEMPTS  # Reset attempts


# Function to reset evidence
def reset_evidence():
    # Delete old evidence before adding new clues

    new_true_clues = [
        f"The culprit was last seen near the {random.choice(locations)}.",
        f"The murder weapon could be a {random.choice(weapons)}.",
        f"{random.choice(suspects)} was acting strangely before the crime."
    ]

    new_false_clues = [
        f"A {random.choice(weapons)} was found, but it may not be related.",
        f"Witnesses suspect {random.choice(suspects)}, but there's no proof.",
        f"The crime might have occurred in {random.choice(locations)}."
    ]

    all_new_clues = new_true_clues + random.sample(new_false_clues, 2)

    for clue in all_new_clues:
        clue_type = "true" if clue in new_true_clues else "false"
        cursor.execute("""
        INSERT INTO evidence (suspect_id, weapon_id, location_id, clue, type)
        VALUES (
            (SELECT id FROM suspects WHERE name = ?),
            (SELECT id FROM weapons WHERE name = ?),
            (SELECT id FROM locations WHERE name = ?),
            ?, ?
            )
        """, (culprit, murder_weapon, crime_location, clue, clue_type))
    conn.commit()


def back(backhome):
    global difficulty
    difficulty = backhome  # Store selected difficulty level
    root.destroy()  # Close the dashboard
    import murderMystery


def show_table():
    show_message("Availabe Table ","EVIDENCE : which helps to get clues.\nSUSPECTS : which shows people involved in murder.\nWEAPONS : which conatins weapons found at crime location.\n LOCATIONS : which contains the locations where the clues where found.",
                 "#2C2F33")


def hints():
    show_message("HINT", "Select * From Evidence;\n\n apply this query to all tables.", "#2C2F33")


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

title_label = tk.Label(root, text="SQL Murder Mystery LEVEL 2", font=("Helvetica", 18, "bold"), fg="white",
                       bg="#23272A")
title_label.pack(pady=10, fill=tk.X)
hint_button = tk.Button(root, text="Hint", command=hints, font=("Arial", 12, "bold"), bg="#99AAB5", fg="black")
hint_button.place(relx=0.9, rely=0.02, anchor="ne")  # Positioned in the top-right corner
query_frame = tk.Frame(root, bg="#2C2F33")
query_frame.pack(pady=20)
query_label = tk.Label(query_frame, text="Enter SQL Query:", font=("Arial", 12), fg="white", bg="#2C2F33")
query_label.pack()
query_entry = tk.Entry(query_frame, width=50, font=("Arial", 12))
query_entry.pack(pady=5)

execute_button = tk.Button(query_frame, text="Execute Query", command=execute_query, font=("Arial", 12), bg="#99AAB5",
                           fg="black")
execute_button.pack(pady=5)
execute_button = tk.Button(query_frame, text="Availabe tables", command=show_table, font=("Arial", 12), bg="#99AAB5",
                           fg="black")
execute_button.pack(pady=5)

output_box = scrolledtext.ScrolledText(root, width=70, height=10, font=("Courier", 10), bg="#2C2F33", fg="white")
output_box.pack(pady=10)

# Frame to align Solve Mystery and Back buttons
button_frame = tk.Frame(root, bg="#2C2F33")
button_frame.pack(pady=10)

# Solve Mystery Button (left side)
solve_button = tk.Button(button_frame, text="Solve the Mystery", command=solve_mystery, font=("Arial", 14, "bold"),
                         bg="#99AAB5", fg="black")
solve_button.pack(side=tk.LEFT, padx=10)

# Back Button (right side)
back_button = tk.Button(button_frame, text="BACK", command=lambda: back("murderMystery"), font=("Arial", 14, "bold"),
                        bg="#99AAB5", fg="black")
back_button.pack(side=tk.RIGHT, padx=10)
root.mainloop()