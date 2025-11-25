# Face Recognition Based Attendance System

An AI-powered attendance automation system using real-time facial recognition, built with Python, OpenCV, face_recognition library, and SQLite.

This project eliminates manual roll-calling, reduces errors, and prevents proxy attendance. It is designed for online/offline classes, including integration with recorded lectures or live webcam feed.

🚀 **Features**
🎦 Real-time Face Detection & Recognition

Uses webcam or screen-recorded video

Automatically identifies students

Marks attendance instantly

👨‍🎓 Student Registration Module

Add new student

Store name, ID, and multiple training images

Saves data into database

🧠 Machine Learning Model

Encodes faces using face_recognition

Trains model automatically on each registration

📅 Attendance Logging

Stores student ID

Timestamp

Date

Prevents duplicate marking

🛢️ SQLite Database Integration

students table

attendance table

train_data folder for images

🖥️ Offline, Lightweight & Fast

No GPU required
Runs smoothly on an Acer Aspire 7 (your laptop)

📂 Project Structure
Face_Attendance_System/
│
├── main.py
├── register_student.py
├── recognize_and_attendance.py
├── encode_faces.py
│
├── /dataset
│      └── student_id/
│             └── images...
│
├── attendance.db
├── requirements.txt
└── README.md