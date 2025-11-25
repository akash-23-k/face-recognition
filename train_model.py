import cv2
import os
import numpy as np
import sqlite3
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
DB_PATH = os.path.join(BASE_DIR, "attendance.db")

MODEL_DIR = os.path.join(BASE_DIR, "trained_model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.yml")
LABELS_PATH = os.path.join(MODEL_DIR, "labels.pkl")


def get_all_students():
    """Fetch all students (name, usn, folder_name) from DB."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, usn, folder_name FROM students")
    data = c.fetchall()
    conn.close()
    return data


def train_model():
    """Train LBPH Face Recognizer on all student images."""
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    label_ids = {}
    current_id = 0
    x_train = []
    y_labels = []

    students = get_all_students()

    if not students:
        print("❌ ERROR: No students found in database!")
        return False

    print("📸 Scanning dataset folders...\n")

    for (name, usn, folder_name) in students:
        student_folder = os.path.join(DATASET_DIR, folder_name)

        if not os.path.exists(student_folder):
            print(f"⚠️ Missing dataset folder for: {name} ({usn})")
            continue

        # Create unique label
        label_ids[folder_name] = {
            "id": current_id,
            "name": name,
            "usn": usn,
            "folder_name": folder_name
        }
        label_id = current_id
        current_id += 1

        # Load all images
        for img_name in os.listdir(student_folder):
            if not img_name.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            img_path = os.path.join(student_folder, img_name)
            img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if img_gray is None:
                continue

            faces = face_cascade.detectMultiScale(img_gray, 1.3, 5)
            for (x, y, w, h) in faces:
                roi = img_gray[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(label_id)

    if len(x_train) == 0:
        print("❌ ERROR: No images found! Collect images first.")
        return False

    # Train the model
    print("🧠 Training LBPH Recognizer...")
    recognizer.train(x_train, np.array(y_labels))

    # Save model
    recognizer.write(MODEL_PATH)
    with open(LABELS_PATH, "wb") as f:
        pickle.dump(label_ids, f)

    print("\n💾 Model saved to:", MODEL_PATH)
    print("💾 Labels saved to:", LABELS_PATH)
    print("🎉 Training complete! Ready for recognition.\n")

    return True


# Run standalone
if __name__ == "__main__":
    train_model()
