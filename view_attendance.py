# view_attendance.py

import sqlite3
from datetime import datetime


DB_PATH = "attendance.db"


def print_table(rows):
    """Print results in a clean table format."""

    if not rows:
        print("⚠️ No attendance records found.")
        return

    print(f"\n{'Name':25} {'USN':12} {'Date':12} {'Status'}")
    print("-" * 60)

    for row in rows:
        name, usn, date, status = row
        print(f"{name:25} {usn:12} {date:12} {status}")


# ---------------- FILTER FUNCTIONS ----------------

def view_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT s.name, a.usn, a.date, a.status 
        FROM attendance a
        JOIN students s ON a.usn = s.usn
        ORDER BY a.date DESC
    """)

    rows = c.fetchall()
    conn.close()
    print_table(rows)


def view_by_usn(usn):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT s.name, a.usn, a.date, a.status 
        FROM attendance a
        JOIN students s ON a.usn = s.usn
        WHERE a.usn=?
        ORDER BY a.date DESC
    """, (usn,))

    rows = c.fetchall()
    conn.close()
    print_table(rows)


def view_by_date(date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT s.name, a.usn, a.date, a.status 
        FROM attendance a
        JOIN students s ON a.usn = s.usn
        WHERE a.date=?
        ORDER BY a.usn
    """, (date,))

    rows = c.fetchall()
    conn.close()
    print_table(rows)


def view_by_month(year, month):
    """Month example: year=2025, month=11"""
    start = f"{year}-{month:02d}-01"
    end = f"{year}-{month:02d}-31"

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT s.name, a.usn, a.date, a.status 
        FROM attendance a
        JOIN students s ON a.usn = s.usn
        WHERE a.date BETWEEN ? AND ?
        ORDER BY a.date DESC
    """, (start, end))

    rows = c.fetchall()
    conn.close()
    print_table(rows)


def view_by_status(status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT s.name, a.usn, a.date, a.status 
        FROM attendance a
        JOIN students s ON a.usn = s.usn
        WHERE a.status=?
        ORDER BY a.date DESC
    """, (status,))

    rows = c.fetchall()
    conn.close()
    print_table(rows)


# ---------------- SIMPLE MENU FOR USER ----------------

def main():
    print("\n====== 📋 VIEW ATTENDANCE ======")
    print("1. View ALL")
    print("2. View by USN")
    print("3. View by Date (YYYY-MM-DD)")
    print("4. View by Month (YYYY MM)")
    print("5. View by Status (Present/Absent)")

    choice = input("\nEnter option (1-5): ").strip()

    if choice == "1":
        view_all()

    elif choice == "2":
        usn = input("Enter USN: ").strip()
        view_by_usn(usn)

    elif choice == "3":
        date = input("Enter date (YYYY-MM-DD): ").strip()
        view_by_date(date)

    elif choice == "4":
        year = int(input("Enter year (YYYY): ").strip())
        month = int(input("Enter month (1-12): ").strip())
        view_by_month(year, month)

    elif choice == "5":
        status = input("Enter status (Present/Absent): ").strip()
        view_by_status(status)

    else:
        print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
