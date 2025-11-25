import cv2
import numpy as np
#import pyautogui
import pickle
import sqlite3
from datetime import datetime
import time

DB_PATH = 'attendance.db'
MODEL_PATH = 'trained_model/model.yml'
LABELS_PATH = 'trained_model/labels.pkl'

# === Load face recognizer model ===
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)

# === Load label mapping ===
with open(LABELS_PATH, 'rb') as f:
    label_mapping = pickle.load(f)

# Update label mapping for folder_name consistency
for label_id, info in label_mapping.items():
    label_mapping[label_id]["folder_name"] = f"{info['name'].replace(' ', '_')}_{info['usn']}"

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def mark_attendance(student_name):
    """Mark attendance only once per day."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute("SELECT id FROM students WHERE name=?", (student_name,))
    result = c.fetchone()
    if result:
        student_id = result[0]
        c.execute("SELECT * FROM attendance WHERE student_id=? AND date=?", (student_id, today))
        if not c.fetchone():
            c.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                      (student_id, today, 'present'))
            conn.commit()
            print(f"✅ Attendance marked for {student_name}")
    conn.close()

# === Define Teams screen capture area ===
#  to Adjust x, y, width, height after checking your Teams gallery position
x, y, width, height = 100, 100, 1000, 600  

print("🎥 Monitoring MS Teams window for faces...")
print("👉 Press 'q' in the preview window to stop")

time.sleep(3)  # Give time to open Teams window

recognized_ids = set()

while True:
    # Capture screenshot region of Teams
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (fx, fy, fw, fh) in faces:
        roi_gray = gray[fy:fy+fh, fx:fx+fw]
        label_id, confidence = recognizer.predict(roi_gray)

        if confidence < 70:  # Lower = better match
            name = label_mapping[label_id]['name']
            usn = label_mapping[label_id]['usn']

            cv2.putText(frame, f"{name} ({usn})", (fx, fy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
            color = (0, 255, 0)

            if label_id not in recognized_ids:
                mark_attendance(name)
                recognized_ids.add(label_id)
        else:
            cv2.putText(frame, "Unknown", (fx, fy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
            color = (0, 0, 255)

        cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), color, 2)

    cv2.imshow("MS Teams Attendance (Press 'q' to quit)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
