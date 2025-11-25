# collect_image.py

import cv2
import os
import sqlite3

DB_PATH = "attendance.db"
DATASET_DIR = "dataset"

def get_student_folder(usn):
    """Fetch student folder_name and name using USN."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, folder_name FROM students WHERE usn=?", (usn,))
    result = c.fetchone()
    conn.close()

    if result:
        return result[0], result[1]  # name, folder_name
    return None, None


def collect_images(usn, num_images=30):
    """Collect images using USN only."""
    name, folder_name = get_student_folder(usn)

    if not name:
        print(f"❌ No student found with USN: {usn}")
        return

    save_path = os.path.join(DATASET_DIR, folder_name)
    os.makedirs(save_path, exist_ok=True)

    print(f"\n🎥 Collecting images for: {name} ({usn})")
    print(f"📁 Saving to: {save_path}")

    cap = cv2.VideoCapture(0)
    count = 0

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera error!")
            break

        cv2.imshow("Collecting Face Images - Press Q to Quit", frame)

        img_name = f"{save_path}/{folder_name}_{count}.jpg"
        cv2.imwrite(img_name, frame)
        count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("⛔ Stopped manually.")
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"✅ Collected {count} images for {name} ({usn})")


# Run directly (optional)
if __name__ == "__main__":
    usn = input("Enter Student USN: ").strip()
    collect_images(usn)
