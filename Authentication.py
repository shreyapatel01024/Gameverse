from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, Frame, PhotoImage, StringVar, messagebox
import mysql.connector
import os
# Database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        #Change your sql Password here
        password="Root@2424",
        #Change Your Database here
        #Firstly Create database ain your mysql and add that here
        #And Create a table with colums as name,username,password
        #Hope So karloge
        database="gameverse"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to database: {err}")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def switch_to_login():
    
    window.title("Login | GameVerse")
    signup_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)


def switch_to_signup():
    window.title("Signup | GameVerse")
    login_frame.pack_forget()
    signup_frame.pack(fill="both", expand=True)


def login():
    username = login_username.get()
    password = login_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Please fill out all fields.")
        return

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful!")
        window.destroy()
        os.system(f"python Home.py {username}")
    else:
        messagebox.showerror("Error", "Invalid username or password.")


def signup():
    name = signup_name.get()
    username = signup_username.get()
    password = signup_password.get()

    if not name or not username or not password:
        messagebox.showerror("Error", "Please fill out all fields.")
        return

    cursor.execute("SELECT * FROM users ")
    usernames = cursor.fetchall()
    gotusername=0
    for user in usernames:
        gotusername = 0
        if(user[2]==username):
            messagebox.showerror("Error","Entered Username is Already Exists, Please Try Something Else")
            gotusername=1
            return
    if(gotusername==0):
        if(username.lower()!=name.lower()):
            if(name.isalpha()):
                cursor.execute("INSERT INTO users (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
                db.commit()
                signup_name.set("")
                signup_username.set("")
                signup_password.set("")
                messagebox.showinfo("Success", "Signup successful! You can now login.")
                switch_to_login()
            else:
                messagebox.showinfo("Error", "Name Should not have Numeric or Special Characters.")

        else:
            messagebox.showinfo("Error", "Name and Username Can't be same.")


# Tkinter window setup
window = Tk()
window.geometry("887x519")
window.configure(bg="#FFFFFF")
window.title("GameVerse")
window.resizable(False, False)

# Variables
login_username = StringVar()
login_password = StringVar()
signup_name = StringVar()
signup_username = StringVar()
signup_password = StringVar()


# Load eye icon images
eye_open_icon = PhotoImage(file=relative_to_assets("unlock.png"))
eye_closed_icon = PhotoImage(file=relative_to_assets("lock.png"))

def toggle_password(entry, button):
    if entry.cget('show') == "*":
        entry.config(show="")
        button.config(image=eye_open_icon)
    else:
        entry.config(show="*")
        button.config(image=eye_closed_icon)

# Login Frame
login_frame = Frame(window, bg="#FFFFFF")
login_canvas = Canvas(
    login_frame,
    bg="#FFFFFF",
    height=519,
    width=887,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)


# Add background image to the purple side of the login frame
login_purple_bg_image = PhotoImage(file=relative_to_assets("Bggameverse.png"))
login_canvas.create_image(653.5, 259.5, image=login_purple_bg_image)  # Center of purple rectangle

Login_entry_image = PhotoImage(file=relative_to_assets("Login_entry_1.png"))

login_canvas.pack(fill="both", expand=True)
#login_canvas.create_rectangle(420.0, 0.0, 887.0, 519.0, fill="#AC10BD", outline="")
login_canvas.create_text(50.0, 66.0, anchor="nw", text="Login", fill="#342E2E", font=("IstokWeb Bold", 30 * -1))
login_canvas.create_rectangle(47.0, 106.0, 80.0, 109.0, fill="#6800BE", outline="")

#LoginUsername
login_canvas.create_text(54.0, 160.0, anchor="nw", text="Username", fill="#000000", font=("IstokWeb Bold", 18 * -1))
login_username_bg = login_canvas.create_image(182.5,215.5,image=Login_entry_image)
login_entry_username = Entry(login_frame, textvariable=login_username, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,
                      font=("IstokWeb", 12))
login_entry_username.place(x=60.0, y=192.0, width=245.0, height=49.0)

#LoginPassword
login_canvas.create_text(54.0, 274.0, anchor="nw", text="Password", fill="#000000", font=("IstokWeb Bold", 18 * -1))
login_password_bg = login_canvas.create_image( 182.5,330.5,image=Login_entry_image)
login_entry_password = Entry(login_frame, textvariable=login_password, show="*", bd=0, bg="#FFFFFF", fg="#000716",
                      highlightthickness=0, font=("IstokWeb", 12))
login_entry_password.place(x=60.0, y=307.0, width=245.0, height=49.0)

# Eye icon button for login
eye_button_login = Button(
    login_frame, image=eye_closed_icon, bd=0, bg="#FFFFFF", activebackground="#FFFFFF",
    command=lambda: toggle_password(login_entry_password, eye_button_login)
)
eye_button_login.place(x=275, y=318, width=30, height=30)  # Adjust placement as needed
#LoginForgetButton
Login_ForgetButton_bg = PhotoImage(file=relative_to_assets("Login_button_1.png"))
Login_ForgetButton = Button( image=Login_ForgetButton_bg,borderwidth=0,highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
Login_ForgetButton.place(x=54.0,y=360.0,width=117.0,height=21.0)


#LoginButton
Login_Button_bg = PhotoImage(file=relative_to_assets("Login_button_2.png"))
Login_button = Button(image=Login_Button_bg, borderwidth=0, highlightthickness=0,
    command=login,
    relief="flat")
Login_button.place(x=111.0, y=414.0, width=121.0, height=42.0)

#SwitchtoSignup
SwitchtoSignup_bg = PhotoImage(file=relative_to_assets("Login_button_3.png"))
SwitchtoSignup_Button = Button(image=SwitchtoSignup_bg,borderwidth=0,highlightthickness=0,
    command=switch_to_signup,
    relief="flat")
SwitchtoSignup_Button.place( x=13.0, y=489.0, width=233.0, height=25.0)


#####################################################################################################################
# Signup Frame
signup_frame = Frame(window, bg="#FFFFFF")
signup_canvas = Canvas(
    signup_frame,
    bg="#FFFFFF",
    height=519,
    width=887,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
#Entry_Bg
signup_entry_image = PhotoImage(file=relative_to_assets("Signup_entry.png"))
signup_canvas.pack(fill="both", expand=True)
# Add background image to the purple side of the signup frame
signup_purple_bg_image = PhotoImage(file=relative_to_assets("Bggameverse.png"))
signup_canvas.create_image(231, 259.5, image=signup_purple_bg_image)  # Center of purple rectangle


#signup_canvas.create_rectangle(0.0, 0.0, 467.0, 519.0, fill="#AC10BD", outline="")
signup_canvas.create_text(521.0, 44.0, anchor="nw", text="SignUp", fill="#342E2E", font=("IstokWeb Bold", 30 * -1))
signup_canvas.create_rectangle(518.0, 84.0, 551.0, 87.0, fill="#6800BE", outline="")

#SignupName
Signup_entry_name_bg = signup_canvas.create_image(653.5,179.5,image=signup_entry_image)
signup_canvas.create_text(524.0, 126.0, anchor="nw", text="Name", fill="#000000", font=("IstokWeb Bold", 18 * -1))
signup_entry_name = Entry(signup_frame, textvariable=signup_name, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,
                       font=("IstokWeb", 12))
signup_entry_name.place(x=531.0, y=160.0, width=245.0, height=43.0)


#SignupUserName
Signup_entry_username_bg = signup_canvas.create_image(653.5,264.5,image=signup_entry_image)
signup_canvas.create_text(524.0, 211.0, anchor="nw", text="Username", fill="#000000", font=("IstokWeb Bold", 18 * -1))
signup_entry_2 = Entry(signup_frame, textvariable=signup_username, bd=0, bg="#FFFFFF", fg="#000716",
                       highlightthickness=0, font=("IstokWeb", 12))
signup_entry_2.place(x=531.0, y=245.0, width=245.0, height=43.0)


#SignupPassword
Signup_entry_password_bg = signup_canvas.create_image(653.5,359.5,image=signup_entry_image)
signup_canvas.create_text(525.0, 306.0, anchor="nw", text="Password", fill="#000000", font=("IstokWeb Bold", 18 * -1))
signup_entry_3 = Entry(signup_frame, textvariable=signup_password, show="*", bd=0, bg="#FFFFFF", fg="#000716",
                       highlightthickness=0, font=("IstokWeb", 12))
signup_entry_3.place(x=531.0, y=340.0, width=245.0, height=43.0)

# Eye icon button for signup
eye_button_signup = Button(
    signup_frame, image=eye_closed_icon, bd=0, bg="#FFFFFF", activebackground="#FFFFFF",
    command=lambda: toggle_password(signup_entry_3, eye_button_signup)
)
eye_button_signup.place(x=750, y=346, width=30, height=30)
#SignupButton

Signup_Button_bg = PhotoImage(file=relative_to_assets("Signup_button_1.png"))
Signup_Button = Button(signup_frame,image=Signup_Button_bg, borderwidth=0,highlightthickness=0,command=signup)
Signup_Button.place(x=582.0,y=405.0,width=121.0,height=42.0)

#SwitchtoLogin
SwitchtoLogin_Button_bg = PhotoImage(file=relative_to_assets("Signup_button_2.png"))
SwitchtoLogin_Button = Button(signup_frame,image=SwitchtoLogin_Button_bg, borderwidth=0,
    highlightthickness=0,
    command=switch_to_login,
    relief="flat"
)
SwitchtoLogin_Button.place(
    x=484.0,
    y=480.0,
    width=250.0,
    height=25.0
)
# Start with the login frame
switch_to_login()
window.mainloop()
