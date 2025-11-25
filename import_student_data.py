import pandas as pd
import sqlite3
import os
from database import add_student, initialize_db

DB_PATH = "attendance.db"
EXCEL_PATH = "student_details.xlsx"
DATASET_DIR = "dataset"


def import_students_from_excel():
    """Import all students from Excel sheet into database."""
    
    # Ensure DB exists
    initialize_db()

    if not os.path.exists(EXCEL_PATH):
        print(f"❌ Excel file not found: {EXCEL_PATH}")
        return

    try:
        df = pd.read_excel(EXCEL_PATH)
    except Exception as e:
        print("❌ Error reading Excel file:", e)
        return

    required_cols = ["USN", "Name", "Department", "Section"]

    # Validate columns
    for col in required_cols:
        if col not in df.columns:
            print(f"❌ Missing required column: {col}")
            return

    print("\n📥 Importing students...")
    print("-" * 50)

    success_count = 0
    skip_count = 0

    for idx, row in df.iterrows():
        usn = str(row["USN"]).strip()
        name = str(row["Name"]).strip()
        department = str(row["Department"]).strip()
        section = str(row["Section"]).strip()

        # Create dataset folder name
        folder_name = f"{name.replace(' ', '_')}_{usn}"
        folder_path = os.path.join(DATASET_DIR, folder_name)

        # Check if student already exists
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT usn FROM students WHERE usn=?", (usn,))
        exists = c.fetchone()
        conn.close()

        if exists:
            print(f"⚠️ Skipping {name} ({usn}) — already exists.")
            skip_count += 1
            continue

        # Add to DB
        add_student(name, usn, department, section)

        # Create dataset folder
        os.makedirs(folder_path, exist_ok=True)

        print(f"✔ Added: {name} ({usn})")
        success_count += 1

    print("-" * 50)
    print(f"🎉 Import complete!")
    print(f"✅ Added: {success_count} students")
    print(f"⚠️ Skipped: {skip_count} (already existed)")
    print("-" * 50)


if __name__ == "__main__":
    import_students_from_excel()
