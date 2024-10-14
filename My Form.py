import sqlite3
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Toplevel, messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Honor\OneDrive\Documents\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Class to add placeholder text functionality
class PlaceholderEntry(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)

        self.add_placeholder()

    def add_placeholder(self, *args):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

    def remove_placeholder(self, *args):
        if self.get() == self.placeholder:
            self.delete(0, 'end')
            self['fg'] = self.default_fg_color


# Function to create a database connection
def create_connection():
    conn = sqlite3.connect("users.db")  # Create a new database if it doesn't exist
    return conn


# Function to create the users table
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


create_table()  # Create the table at the start

# Store the registration data
registration_data = {
    "username": "",
    "email": "",
    "password": "",
    "confirm_password": ""
}

# Store the login data
login_data = {
    "username": "",
    "password": ""
}


# Function to handle registration button click
def handle_registration():
    global registration_data
    registration_data['username'] = entry_1.get()
    registration_data['email'] = entry_2.get()
    registration_data['password'] = entry_3.get()
    registration_data['confirm_password'] = entry_4.get()

    # Ensure no fields are empty and passwords match
    if not registration_data['username'] or not registration_data['password']:
        messagebox.showerror("Error", "Username and Password cannot be empty!")
        return
    elif registration_data['password'] != registration_data['confirm_password']:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    try:
        # Insert data into the database
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        ''', (registration_data['username'], registration_data['email'], registration_data['password']))
        conn.commit()
        conn.close()
        print("Registration successful!")
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to handle login button click
def handle_login():
    global login_data
    login_data['username'] = login_entry_1.get()
    login_data['password'] = login_entry_2.get()

    # Ensure no fields are empty
    if not login_data['username'] or not login_data['password']:
        messagebox.showerror("Error", "Username and Password cannot be empty!")
        return

    # Verify login credentials
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
    ''', (login_data['username'], login_data['password']))
    user = cursor.fetchone()
    conn.close()

    if user:
        print("Login successful!")
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password!")


# Function to open the login form
def open_login_form():
    window.withdraw()  # Hide the main registration window

    login_window = Toplevel()
    login_window.geometry("391x286")
    login_window.configure(bg="#2AE6CF")
    login_window.title("Login")

    login_canvas = Canvas(
        login_window,
        bg="#2AE6CF",
        height=286,
        width=391,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    login_canvas.place(x=0, y=0)
    login_canvas.create_text(
        130.0,
        15.0,
        anchor="nw",
        text="Login Form",
        fill="#0D0C0C",
        font=("Inter Bold", 20 * -1)
    )

    # Username Entry
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    login_canvas.create_image(274.5, 88.0, image=entry_image_1)

    global login_entry_1  # Declare login_entry_1 as global
    login_entry_1 = Entry(login_window, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    login_entry_1.place(x=192.0, y=75.0, width=165.0, height=24.0)

    # Password Entry
    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    login_canvas.create_image(274.5, 146.0, image=entry_image_2)

    global login_entry_2  # Declare login_entry_2 as global
    login_entry_2 = Entry(login_window, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, show="*")
    login_entry_2.place(x=192.0, y=133.0, width=165.0, height=24.0)

    login_canvas.create_text(
        41.0,
        78.0,
        anchor="nw",
        text="Username:",
        fill="#1E1E1E",
        font=("Inter Bold", 20 * -1)
    )

    login_canvas.create_text(
        48.0,
        133.0,
        anchor="nw",
        text="Password:",
        fill="#0D0C0C",
        font=("Inter Bold", 20 * -1)
    )

    # Standard Login Button
    login_button_1 = Button(
        login_window,
        text="Login",
        command=handle_login,  # Call handle_login function on click
        relief="flat",
        bg="#4CAF50",
        fg="white"
    )
    login_button_1.place(x=138.0, y=212.0, width=92.0, height=30.0)

    # Button to go back to the registration form
    back_to_registration_button = Button(
        login_window,
        text="Back to Registration",
        command=lambda: (login_window.destroy(), window.deiconify()),  # Hide login window and show registration window
        relief="flat",
        bg="#F44336",
        fg="white"
    )
    back_to_registration_button.place(x=115.0, y=250.0, width=160.0, height=30.0)


# Main registration form window
window = Tk()
window.geometry("758x550")
window.configure(bg="#21E0C9")
window.title("Registration")

canvas = Canvas(
    window,
    bg="#21E0C9",
    height=550,
    width=758,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Title for Registration Form
canvas.create_text(227.0, 26.0, anchor="nw", text="REGISTRATION FORM", fill="#000000", font=("Inter SemiBold", 32 * -1))

# Username entry with placeholder
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
canvas.create_image(509.5, 120.0, image=entry_image_1)
entry_1 = PlaceholderEntry(window, placeholder="Enter Username", bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_1.place(x=413.0, y=105.0, width=193.0, height=28.0)
canvas.create_text(193.0, 106.0, anchor="nw", text="Username:", fill="#000000", font=("Inter", 24 * -1))

# Email entry with placeholder
entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
canvas.create_image(509.0, 183.0, image=entry_image_2)
entry_2 = PlaceholderEntry(window, placeholder="Enter Email", bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_2.place(x=413.0, y=168.0, width=192.0, height=28.0)
canvas.create_text(249.0, 166.0, anchor="nw", text="Email:", fill="#000000", font=("Inter", 24 * -1))

# Password entry with placeholder
entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
canvas.create_image(509.0, 246.0, image=entry_image_3)
entry_3 = PlaceholderEntry(window, placeholder="Enter Password", bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0,
                           show="*")
entry_3.place(x=413.0, y=231.0, width=192.0, height=28.0)
canvas.create_text(204.0, 231.0, anchor="nw", text="Password:", fill="#000000", font=("Inter", 24 * -1))

# Confirm Password entry with placeholder
entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
canvas.create_image(509.0, 316.0, image=entry_image_4)
entry_4 = PlaceholderEntry(window, placeholder="Enter Password", bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0,
                           show="*")
entry_4.place(x=413.0, y=301.0, width=192.0, height=28.0)
canvas.create_text(106.0, 301.0, anchor="nw", text="Confirm Password:", fill="#000000", font=("Inter", 24 * -1))

# Standard Submit Button for registration
submit_button = Button(
    window,
    text="Register",
    command=handle_registration,  # Call handle_registration on click
    relief="flat",
    bg="#4CAF50",
    fg="white"
)
submit_button.place(x=315.0, y=385.0, width=103.0, height=32.0)

# Login button for existing account
canvas.create_text(379.0, 492.0, anchor="nw", text="for existing account", fill="#000000",
                   font=("Inter Italic", 16 * -1))
login_button_2 = Button(
    window,
    text="Login",
    command=open_login_form,  # Open login form on click
    relief="flat",
    bg="#4CAF50",
    fg="white"
)
login_button_2.place(x=284.0, y=486.0, width=82.0, height=31.0)

window.resizable(True, True)
window.mainloop()
