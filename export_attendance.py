import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

DB_PATH = "attendance.db"
EXPORT_DIR = "exports"


# --------------------- Helper: Choose Format ---------------------

def choose_export_format():
    print("\n📤 Choose Export Format:")
    print("1. Excel (.xlsx)")
    print("2. CSV (.csv)")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        return "excel"
    elif choice == "2":
        return "csv"
    else:
        print("❌ Invalid option, defaulting to Excel.")
        return "excel"


# --------------------- Core Export Function ---------------------

def export_attendance(start_date, end_date, label, file_format):
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    conn = sqlite3.connect(DB_PATH)
    query = f"""
        SELECT * FROM attendance 
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY date
    """

    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        print("❌ Error reading database:", e)
        conn.close()
        return

    conn.close()

    if df.empty:
        print(f"⚠️ No attendance found between {start_date} and {end_date}")
        return

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    filename = f"{label}_{timestamp}"

    if file_format == "excel":
        file_path = os.path.join(EXPORT_DIR, f"{filename}.xlsx")
        df.to_excel(file_path, index=False)
    else:
        file_path = os.path.join(EXPORT_DIR, f"{filename}.csv")
        df.to_csv(file_path, index=False)

    print("\n✅ Export Successful!")
    print(f"📁 Saved as: {file_path}")
    print(f"📊 Total Records: {len(df)}")


# --------------------- Export Modes ---------------------

def export_daily(file_format):
    today = datetime.now().strftime("%Y-%m-%d")
    export_attendance(today, today, f"Daily_{today}", file_format)


def export_weekly(file_format):
    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())   # Monday
    end = start + timedelta(days=6)                   # Sunday
    export_attendance(start, end, f"Weekly_{start}_to_{end}", file_format)


def export_monthly(file_format):
    today = datetime.now().date()
    start = today.replace(day=1)
    next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
    end = next_month - timedelta(days=1)
    label = f"Monthly_{today.strftime('%Y_%m')}"
    export_attendance(start, end, label, file_format)


def export_custom(file_format):
    start = input("Enter start date (YYYY-MM-DD): ").strip()
    end = input("Enter end date (YYYY-MM-DD): ").strip()
    label = f"Custom_{start}_to_{end}"
    export_attendance(start, end, label, file_format)


# --------------------- CLI Menu (Optional) ---------------------

def main():
    print("====== 🧾 ATTENDANCE EXPORT TOOL ======")
    print("1. Export Today's Attendance")
    print("2. Export This Week")
    print("3. Export This Month")
    print("4. Export Custom Date Range")

    choice = input("\nEnter choice (1-4): ").strip()
    file_format = choose_export_format()

    if choice == "1":
        export_daily(file_format)
    elif choice == "2":
        export_weekly(file_format)
    elif choice == "3":
        export_monthly(file_format)
    elif choice == "4":
        export_custom(file_format)
    else:
        print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
