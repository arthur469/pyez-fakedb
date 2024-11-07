import sqlite3
import logging
from faker import Faker
from sqlite3 import Error
import argparse
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import random
import string
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_database(db_path: str):
    """
    Creates a SQLite database and a 'users' table with additional fields.
    
    :param db_path: Path to the database file.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                age INTEGER,
                birth_year INTEGER,
                city TEXT,
                zip_code TEXT,
                country TEXT,
                phone_number TEXT,
                address TEXT,
                job TEXT,
                company TEXT
            )
        ''')

        conn.commit()
        logging.info(f'Database "{db_path}" and table "users" created successfully.')
    except Error as e:
        logging.error(f"Error creating the database: {e}")
    finally:
        if conn:
            conn.close()

def generate_random_password(length=10):
    """
    Generates a random password.
    
    :param length: Length of the password (default 10).
    :return: Randomly generated password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def populate_database(db_path: str, num_entries: int, replace=False):
    """
    Populates the database with fake data for additional fields.
    
    :param db_path: Path to the database file.
    :param num_entries: Number of fake entries to add.
    :param replace: Replace existing data if True.
    """
    fake = Faker()
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if replace:
            cursor.execute("DELETE FROM users")

        for _ in range(num_entries):
            user_id = fake.uuid4()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            password = generate_random_password()
            age = fake.random_int(min=18, max=90)
            birth_year = fake.date_of_birth(minimum_age=18, maximum_age=90).year
            city = fake.city()
            zip_code = fake.zipcode()
            country = fake.country()
            phone_number = fake.phone_number()
            address = fake.address()
            job = fake.job()
            company = fake.company()

            cursor.execute('''
                INSERT INTO users (
                    user_id, first_name, last_name, email, password,
                    age, birth_year, city, zip_code, country,
                    phone_number, address, job, company
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, first_name, last_name, email, password,
                  age, birth_year, city, zip_code, country,
                  phone_number, address, job, company))

        conn.commit()
        logging.info(f'{num_entries} fake users added to the database "{db_path}".')
    except Error as e:
        logging.error(f"Error populating the database: {e}")
    finally:
        if conn:
            conn.close()

def run_with_gui():
    """
    Runs the program with a graphical interface to input the number of entries and the database name.
    """
    def on_submit():
        try:
            num_entries = int(entry_num.get())
            database_name = entry_db.get() or "test_database"
            folder_path = entry_folder.get() or "db"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            db_path = os.path.join(folder_path, f'{database_name}.db')
            if os.path.exists(db_path):
                top = tk.Toplevel(root)
                top.title("Existing Database")
                tk.Label(top, text="The database already exists. What would you like to do?").pack(pady=10)
                
                def add_data():
                    populate_database(db_path, num_entries)
                    top.destroy()
                
                def replace_data():
                    populate_database(db_path, num_entries, replace=True)
                    top.destroy()
                
                def cancel():
                    top.destroy()
                
                tk.Button(top, text="Add", command=add_data).pack(side=tk.LEFT, padx=5, pady=5)
                tk.Button(top, text="Replace", command=replace_data).pack(side=tk.LEFT, padx=5, pady=5)
                tk.Button(top, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5, pady=5)
            else:
                create_database(db_path)
                populate_database(db_path, num_entries)
                messagebox.showinfo("Success", f"{num_entries} entries added to the database.")
        except ValueError:
            messagebox.showerror("Invalid Entry", "Please enter a valid number.")
        except Error as e:
            messagebox.showerror("Error", f"Error creating the database: {e}")

    root = tk.Tk()
    root.title("Database Entry Generator")

    tk.Label(root, text="Number of entries to create:").pack(pady=10)
    entry_num = tk.Entry(root)
    entry_num.pack(pady=5)
    entry_num.insert(0, "100")  # Default value

    tk.Label(root, text="Database name:").pack(pady=10)
    entry_db = tk.Entry(root)
    entry_db.pack(pady=5)
    entry_db.insert(0, "test_database")  # Default value

    def select_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry_folder.delete(0, tk.END)
            entry_folder.insert(0, folder_selected)

    tk.Label(root, text="Select folder (optional):").pack(pady=10)
    entry_folder = tk.Entry(root)
    entry_folder.pack(pady=5)
    entry_folder.insert(0, "db")  # Default value
    tk.Button(root, text="Browse", command=select_folder).pack(pady=5)

    tk.Button(root, text="Generate", command=on_submit).pack(pady=20)

    root.mainloop()

def run_with_cli(num_entries: int, db_name: str, folder_path: str):
    """
    Runs the program with CLI input for the number of entries.
    
    :param num_entries: Number of entries specified by the user.
    :param db_name: Name of the database file.
    :param folder_path: Path to the database folder.
    """
    db_path = os.path.join(folder_path, f'{db_name}.db')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if os.path.exists(db_path):
        response = input("The database already exists. Do you want to add data (a), replace data (r) or cancel (c)? ").strip().lower()
        if response == 'c':
            return
        elif response == 'a':
            populate_database(db_path, num_entries)
        elif response == 'r':
            populate_database(db_path, num_entries, replace=True)
        else:
            print("Invalid response. Canceling.")
            return
    else:
        create_database(db_path)
        populate_database(db_path, num_entries)
    logging.info("Database population completed.")

def main():
    """
    Main function to parse command line arguments and choose CLI or GUI.
    """
    parser = argparse.ArgumentParser(description="Populate a database with fake user data.")
    parser.add_argument(
        "-n", "--num_entries",
        type=int,
        help="Number of entries to create (default: 100)"
    )
    parser.add_argument(
        "-d", "--database_name",
        type=str,
        default="test_database",
        help="Name of the database file (default: test_database)"
    )
    parser.add_argument(
        "-f", "--folder_path",
        type=str,
        default="db",
        help="Path to the database folder (default: db)"
    )
    args = parser.parse_args()

    if args.num_entries is not None:
        run_with_cli(args.num_entries, args.database_name, args.folder_path)
    else:
        run_with_gui()

if __name__ == '__main__':
    main()
