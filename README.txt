<p align="center">
  <h1 align="center">🚗 Parking Lot System</h1>
  <p align="center">
    CS15 • Python • Django Web Application
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Django-5.x-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" />
</p>

---

## 📌 Overview

The **Parking Lot System** is a web-based application developed using **Python and Django**.  
It automates parking operations such as vehicle check-in, check-out, slot allocation, and real-time billing.

The system is designed with a focus on **usability**, **clarity**, and **real-world workflow simulation**, making it suitable for both academic and practical use.

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
- Billing duration is rounded up to the next hour

### 📄 Session Details
- Displays plate number, slot, duration, and billing summary
- Updates billing information dynamically for active sessions

### 🛠️ Administration
- Uses Django’s built-in admin panel
- Manage parking slots and sessions easily

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
| Frontend | HTML, CSS (Django Templates) |
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

yaml
Copy code

---

## 🚀 Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Feliciety02/Parking-Lot-System-CS15-Python.git
cd Parking-Lot-System-CS15-Python
2. Create and Activate Virtual Environment
bash
Copy code
python -m venv venv
Windows

bash
Copy code
venv\Scripts\activate
macOS / Linux

bash
Copy code
source venv/bin/activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Apply Database Migrations
bash
Copy code
python manage.py migrate
5. Run the Development Server
bash
Copy code
python manage.py runserver
Access the application at:

cpp
Copy code
http://127.0.0.1:8000/
💰 Billing Rules
Parking is billed per hour

Minimum billing is one hour

Duration is rounded up to the next hour

Examples

33 minutes → billed as 1 hour

1 hour 10 minutes → billed as 2 hours

🔮 Future Enhancements
Online payment integration

Visual parking slot map

Mobile-responsive interface

QR code or RFID-based check-in

Role-based access control

📜 License
This project is licensed under the MIT License.

👤 Author
Developed as part of the CS15 Python Course Project
Designed with emphasis on clean UI, correct logic, and real-world workflows.
