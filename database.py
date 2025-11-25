import sqlite3
import os

DB_NAME = 'attendance.db'
DATASET_DIR = 'dataset'

def initialize_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Correct students table (matches train_model.py)
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            usn TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT,
            section TEXT,
            folder_name TEXT NOT NULL
        )
    ''')

    # Correct attendance table (uses USN, not student_id)
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT,
            date TEXT,
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized and ready.")


def add_student(name, usn, department="", section="A"):
    """Add a new student to the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    folder_name = f"{name.replace(' ', '_')}_{usn}"
    student_folder = os.path.join(DATASET_DIR, folder_name)
    os.makedirs(student_folder, exist_ok=True)

    try:
        c.execute(
            "INSERT INTO students (usn, name, department, section, folder_name) VALUES (?, ?, ?, ?, ?)",
            (usn, name, department, section, folder_name)
        )
        conn.commit()
        print(f"🎉 Student '{name}' ({usn}) added successfully!")
        print(f"📁 Dataset folder created: {student_folder}")

    except sqlite3.IntegrityError:
        print(f"⚠️ Student with USN {usn} already exists.")

    conn.close()


if __name__ == "__main__":
    initialize_db()

    print("\n--- Add New Student ---")
    name = input("Enter student name: ").strip()
    usn = input("Enter student USN: ").strip()
    department = input("Enter department (optional): ").strip()
    section = input("Enter section (default A): ").strip() or "A"

    add_student(name, usn, department, section)
    