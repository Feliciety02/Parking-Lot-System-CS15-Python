# 🚗 Parking Lot System

**CS15 – Python | Django Web Application**

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-5.x-green)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

The **Parking Lot System** is a web-based application developed using **Python and Django**.  
It automates parking operations such as vehicle check-in, check-out, slot allocation, and real-time billing.

The system is designed with a focus on **usability**, **clarity**, and **real-world workflow simulation**, making it suitable for academic and practical use.

---

## ✨ Features

### 🚘 Vehicle Check-In
- Input vehicle plate number
- Select from available parking slots only
- Automatically records time-in

### 💵 Vehicle Check-Out
- Select an active parking session
- Displays real-time duration and amount due
- Accepts cash payment and calculates change

### ⏱️ Real-Time Billing
- Fixed hourly rate
- Minimum billing of one hour
- Duration rounded up to the next hour

### 📄 Session Details
- Displays plate number, slot, duration, and billing summary
- Updates billing information dynamically for active sessions

### 🛠️ Administration
- Uses Django’s built-in admin panel
- Manage parking data efficiently

---

## 🔄 System Workflow

### Check-In Process
1. Enter vehicle plate number  
2. Select an available parking slot  
3. System records time-in and marks the slot as occupied  

### Check-Out Process
1. Select a parked vehicle  
2. System computes duration and amount due  
3. Enter cash received  
4. System calculates change and completes the session  

---

## 🧰 Technology Stack

| Layer | Technology |
|------|-----------|
| Backend | Python (Django) |
| Frontend | HTML, CSS |
| Database | SQLite |
| Architecture | Model–View–Template (MVT) |

---

## 📁 Project Structure

Parking-Lot-System-CS15-Python/
│
├── parking/
│ ├── migrations/
│ ├── templates/
│ ├── static/
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ └── urls.py
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

---

## 🚀 Installation and Setup

### 1. Clone the Repository
```bash

git clone https://github.com/Feliciety02/Parking-Lot-System-CS15-Python.git
cd Parking-Lot-System-CS15-Python
2. Create and Activate Virtual Environment
python -m venv venv
Windows

venv\Scripts\activate
macOS / Linux


source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt

4. Apply Database Migrations
python manage.py migrate

5. Run the Development Server
python manage.py runserver

Open in browser:
http://127.0.0.1:8000/

💰 Billing Rules
Parking is billed per hour

Minimum billing is one hour

Duration is rounded up to the next hour

Examples

33 minutes → billed as 1 hour

1 hour 10 minutes → billed as 2 hours

🔮 Future Improvements
Online payment integration

Visual parking slot map

Mobile-responsive interface

QR code or RFID-based check-in

Role-based access control

📜 License
This project is licensed under the MIT License.

👤 Author
Developed as part of the CS15 Python Course Project.
Focused on practical system design, usability, and clean interface layout.
