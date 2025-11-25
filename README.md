# 🎓 Face Recognition Based Attendance System  
A fully automated attendance system using LBPH face recognition, OpenCV, and SQLite database — designed for real-time classroom use.
 <!-- Optional image -->
<img width="1536" height="1024" alt="ChatGPT Image Nov 25, 2025, 09_22_24 AM" src="https://github.com/user-attachments/assets/c4fcf05a-c617-4872-a1b3-27c92898289f" />

---

## 🚀 Features

- 📥 **Import Student Data** from Excel  
- 📸 **Capture Student Images** and automatically generate datasets  
- 🧠 **Train LBPH Model** using student face images  
- 👤 **Real-time Face Recognition** with auto attendance marking  
- 🗂️ **SQLite Database** (Students + Attendance)  
- 📊 **Export Attendance Report** in Excel format  
- 🧾 **Admin Menu (app.py)** — single menu-driven control  
- 🧱 **Modular Functions** (clean project architecture)

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **OpenCV (cv2)**
- **NumPy**
- **Pandas**
- **SQLite3**
- **Pickle**
- **OS / File handling**

---

## 📂 Project Structure

face_attendance_system/
│── app.py
│── collect_images.py
│── train_model.py
│── recognize_and_attendance.py
│── import_student_data.py
│── view_attendance.py
│── export_attendance.py
│── database.py
│── attendance.db
│── student_details.xlsx
│── dataset/
│ └── Name_USN/
│ └── images...
│── trained_model/
│ ├── model.yml
│ └── labels.pkl
│── README.md

## 🧩 Workflow

### 1️⃣ Import Student Data  
Upload `student_details.xlsx` containing:  
`USN | Name | Department | Section`

### 2️⃣ Collect Student Images  
System captures 50–100 images per student.

### 3️⃣ Train Model  
LBPH training generates:  
- `model.yml`  
- `labels.pkl`

### 4️⃣ Recognize & Mark Attendance  
Face detected → Match → Attendance stored in DB.

### 5️⃣ View or Export Attendance  
Report includes:  
`USN | Name | Department | Section | Date | Status`

---

## 🖼️ System Architecture (DFD + ERD)
<img width="2816" height="1536" alt="Gemini_Generated_Image_xuhx0exuhx0exuhx" src="https://github.com/user-attachments/assets/ce6164ea-1567-48a1-83a7-1e8ce325b6bd" />
<img width="2816" height="1536" alt="Gemini_Generated_Image_ar994zar994zar99" src="https://github.com/user-attachments/assets/5cbe7d60-4c3f-4a24-8c6a-9954a1082751" />
<img width="2816" height="1536" alt="Gemini_Generated_Image_2jlsnj2jlsnj2jls" src="https://github.com/user-attachments/assets/e4ed2053-0461-4453-a2f2-0a6617383b61" />


## 🧪 Requirements

pip install opencv-python
pip install numpy
pip install pandas

## ▶️ Run the System

Run master controller:

python app.py

From here you can:

1. Import student data  
2. Capture images  
3. Train model  
4. Run recognition  
5. View attendance  
6. Export report  
7. Exit  

---

## 📤 Export Attendance

Exports automatically to:

Attendance_Report.xlsx

## 🛡️ Disclaimer  
This project is for **learning and academic purposes**.

---

## ⭐ Show Your Support  
Give a ⭐ on GitHub if you found this helpful!
