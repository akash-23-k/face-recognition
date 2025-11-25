import cv2
import sqlite3
import pickle
from datetime import datetime
import os

DB_PATH = "attendance.db"
MODEL_PATH = "trained_model/model.yml"
LABELS_PATH = "trained_model/labels.pkl"


def load_labels():
    """Load label mappings from labels.pkl."""
    if not os.path.exists(LABELS_PATH):
        print("❌ labels.pkl not found! Train model first.")
        return None

    with open(LABELS_PATH, "rb") as f:
        return pickle.load(f)


def mark_attendance(usn):
    """Mark attendance using USN only (simple mode)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    # Check if attendance already marked
    c.execute("SELECT * FROM attendance WHERE usn=? AND date=?", (usn, today))
    exists = c.fetchone()

    if not exists:
        c.execute("INSERT INTO attendance (usn, date, status) VALUES (?, ?, ?)",
                  (usn, today, "Present"))
        conn.commit()
        print(f"✅ Attendance marked for USN: {usn}")

    conn.close()


def start_recognition():
    """Start camera and recognize faces in real time."""
    print("🔄 Loading recognition model...")

    if not os.path.exists(MODEL_PATH):
        print("❌ Model not found! Train model first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    labels = load_labels()
    if labels is None:
        return

    # Reverse lookup: label_id → student info
    id_to_student = {v["id"]: v for v in labels.values()}

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)
    recognized_usns = set()

    print("🎥 Recognition started. Press 'q' to exit.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera error!")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y + h, x:x + w]

            label_id, confidence = recognizer.predict(roi)

            if confidence < 70:
                if label_id in id_to_student:
                    student = id_to_student[label_id]
                    name, usn = student["name"], student["usn"]

                    cv2.putText(frame, f"{name} ({usn})",
                                (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 255, 0), 2)

                    color = (0, 255, 0)

                    if usn not in recognized_usns:
                        mark_attendance(usn)
                        recognized_usns.add(usn)
                else:
                    cv2.putText(frame, "Unknown", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 0, 255), 2)
                    color = (0, 0, 255)
            else:
                cv2.putText(frame, "Unknown", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 0, 255), 2)
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        cv2.imshow("Face Recognition - Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\n🛑 Recognition stopped.")


# Run standalone
if __name__ == "__main__":
    start_recognition()
