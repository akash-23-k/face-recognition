import os
from database import initialize_db, add_student
from import_student_data import import_students_from_excel
from collect_images import collect_images
from train_model import train_model
from recognize_and_attendance import start_recognition
from view_attendance import view_all, view_by_status
from export_attendance import (
    export_daily, export_weekly,
    export_monthly, export_custom,
    choose_export_format
)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress ENTER to continue...")


def menu():
    while True:
        clear_screen()

        print("==========================================")
        print("   FACE RECOGNITION ATTENDANCE SYSTEM")
        print("==========================================\n")

        print("1. Initialize Database")
        print("2. Import Students from Excel (student_details.xlsx)")
        print("3. Add Student Manually")
        print("4. Collect Images")
        print("5. Train Model")
        print("6. Start Recognition")
        print("7. View Attendance")
        print("8. Export Attendance")
        print("9. Exit")

        choice = input("\nEnter choice: ").strip()

        # ----------------- OPTIONS -----------------

        if choice == "1":
            initialize_db()
            pause()

        elif choice == "2":
            print("\n📂 Importing from student_details.xlsx ...")
            import_students_from_excel("student_details.xlsx")
            pause()

        elif choice == "3":
            name = input("Enter student name: ").strip()
            usn = input("Enter student USN: ").strip()
            dept = input("Enter department (optional): ").strip()
            sec = input("Enter section (default A): ").strip() or "A"
            add_student(name, usn, dept, sec)
            pause()

        elif choice == "4":
            folder_name = input("Enter exact student folder name (e.g., Akash_Kumar_Soni_221030039): ").strip()
            collect_images(folder_name)
            pause()

        elif choice == "5":
            train_model()
            pause()

        elif choice == "6":
            start_recognition()
            pause()

        elif choice == "7":
            print("\n1. View All Attendance")
            print("2. View by Status (Present/Absent)")
            sub = input("Enter choice: ").strip()

            if sub == "1":
                view_all()
            elif sub == "2":
                view_by_status()
            else:
                print("❌ Invalid option.")
            pause()

        elif choice == "8":
            print("\n📤 Export Options:")
            print("1. Daily")
            print("2. Weekly")
            print("3. Monthly")
            print("4. Custom Range")

            sub = input("Enter choice: ").strip()

            if sub == "1":
                export_daily()
            elif sub == "2":
                export_weekly()
            elif sub == "3":
                export_monthly()
            elif sub == "4":
                export_custom()
            else:
                print("❌ Invalid option.")
            pause()

        elif choice == "9":
            print("\n👋 Exiting system. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")
            pause()


if __name__ == "__main__":
    menu()
