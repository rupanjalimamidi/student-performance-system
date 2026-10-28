# Student Performance Tracking System

A web-based application for managing student information and tracking academic performance using Python Flask and SQLite.

## 📌 Project Overview

The Student Performance Tracking System provides a centralized platform to manage student records, subject-wise marks, attendance, and academic performance. It automatically calculates average marks, attendance percentages, and grades, while the dashboard displays performance statistics and a subject-wise chart.

## ✨ Key Features

- Administrator login
- Student registration and management
- Department and academic year selection
- Subject-wise marks and attendance entry
- Individual student performance summaries
- Automatic average marks and attendance calculations
- Grade generation based on average marks
- Dashboard statistics and subject-wise performance chart
- SQLite database for storing records

## 🛠️ Technology Stack

- Backend: Python, Flask
-Frontend: HTML, CSS
- Database: SQLite
-Development Tool: Visual Studio Code

## 📁 Project Structure

```text
student-performance-system/
├── app.py
├── requirements.txt
├── database.db
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── login.html
    ├── dashboard.html
    ├── students.html
    ├── add_student.html
    ├── performance.html
    └── student_performance.html
```

## 🚀 How to Run Locally

1. Install Python 3.11 or a compatible version.
2. Clone this repository:

   ```bash
   git clone https://github.com/rupanjalimamidi/student-performance-system.git
   ```

3. Open the project folder:

   ```bash
   cd student-performance-system
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

## 🔐 Demo Login

- **Username:** `admin`
- **Password:** `admin123`

These are demonstration credentials for the prototype, not production-ready authentication.

## 🔮 Future Enhancements

- Downloadable academic reports
- Search and filtering options
- Role-based access for administrators, faculty, and students
- Enhanced authentication and security
- Advanced performance analytics

## 👩‍💻 Project Author

**Mamidi Hitesh**

## 📄 License

This project was developed for educational and prototype demonstration purposes.
