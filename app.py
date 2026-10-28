from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    conn = get_db_connection()

    # Students table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    """)

    # Performance table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            marks REAL NOT NULL,
            attendance REAL NOT NULL,
            FOREIGN KEY (student_id)
                REFERENCES students(student_id)
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# LOGIN
# =========================================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            return redirect(
                url_for("dashboard")
            )

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    conn = get_db_connection()

    # -----------------------------------------------------
    # Get all students
    # -----------------------------------------------------

    students = conn.execute("""
        SELECT *
        FROM students
        ORDER BY id DESC
    """).fetchall()

    # -----------------------------------------------------
    # Get all performance records
    # -----------------------------------------------------

    records = conn.execute("""
        SELECT
            student_id,
            subject,
            marks,
            attendance
        FROM performance
    """).fetchall()

    conn.close()

    # =====================================================
    # SUBJECT MAPPING
    # =====================================================

    subject_mapping = {

        "python": [
            "Python"
        ],

        "dbms": [
            "DBMS"
        ],

        "web": [
            "Web Development",
            "Web"
        ],

        "dsa": [
            "Data Structures & Algorithms",
            "DSA"
        ],

        "cyber": [
            "Cyber Technology",
            "Cyber Security",
            "Cyber"
        ],

        "networks": [
            "Computer Networks",
            "Networks"
        ]
    }

    # =====================================================
    # CALCULATE SUBJECT AVERAGES
    # =====================================================

    chart_values = {}

    for chart_subject, database_subjects in subject_mapping.items():

        marks = []

        for record in records:

            if record["subject"] in database_subjects:

                marks.append(
                    float(record["marks"])
                )

        if marks:

            chart_values[chart_subject] = round(
                sum(marks) / len(marks),
                1
            )

        else:

            chart_values[chart_subject] = 0

    # =====================================================
    # TOTAL STUDENTS
    # =====================================================

    total_students = len(students)

    # =====================================================
    # OVERALL PERFORMANCE
    # =====================================================

    if records:

        average_performance = round(
            sum(
                float(record["marks"])
                for record in records
            ) / len(records),
            1
        )

        average_attendance = round(
            sum(
                float(record["attendance"])
                for record in records
            ) / len(records),
            1
        )

    else:

        average_performance = 0
        average_attendance = 0

    # =====================================================
    # STUDENTS NEEDING ATTENTION
    # =====================================================

    need_attention = 0

    for student in students:

        student_records = [
            record
            for record in records
            if record["student_id"]
            == student["student_id"]
        ]

        if student_records:

            student_average = sum(
                float(record["marks"])
                for record in student_records
            ) / len(student_records)

            student_attendance = sum(
                float(record["attendance"])
                for record in student_records
            ) / len(student_records)

            # Student needs attention if:
            # marks below 50 OR attendance below 75

            if (
                student_average < 50
                or student_attendance < 75
            ):
                need_attention += 1

    # =====================================================
    # SEND DATA TO DASHBOARD
    # =====================================================

    return render_template(

        "dashboard.html",

        students=students,

        total_students=total_students,

        average_performance=average_performance,

        average_attendance=average_attendance,

        need_attention=need_attention,

        chart_values=chart_values
    )


# =========================================================
# STUDENTS
# =========================================================

@app.route("/students")
def students():

    conn = get_db_connection()

    students = conn.execute("""
        SELECT *
        FROM students
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students
    )


# =========================================================
# ADD STUDENT
# =========================================================

@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]

        student_id = request.form["student_id"]

        department = request.form["department"]

        year = request.form["year"]

        email = request.form["email"]

        phone = request.form["phone"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO students
            (
                name,
                student_id,
                department,
                year,
                email,
                phone
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            student_id,
            department,
            year,
            email,
            phone
        ))

        conn.commit()

        conn.close()

        return redirect(
            url_for("students")
        )

    return render_template(
        "add_student.html"
    )


# =========================================================
# PERFORMANCE - STUDENT LIST
# =========================================================

@app.route("/performance")
def performance():

    conn = get_db_connection()

    students = conn.execute("""
        SELECT *
        FROM students
        ORDER BY name
    """).fetchall()

    conn.close()

    return render_template(
        "performance.html",
        students=students
    )


# =========================================================
# INDIVIDUAL STUDENT PERFORMANCE
# =========================================================

@app.route(
    "/student-performance/<student_id>",
    methods=["GET", "POST"]
)
def student_performance(student_id):

    conn = get_db_connection()

    # -----------------------------------------------------
    # Get student
    # -----------------------------------------------------

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE student_id = ?
    """, (
        student_id,
    )).fetchone()

    if student is None:

        conn.close()

        return "Student not found", 404

    # -----------------------------------------------------
    # Add performance record
    # -----------------------------------------------------

    if request.method == "POST":

        subject = request.form["subject"]

        marks = float(
            request.form["marks"]
        )

        attendance_value = float(
            request.form["attendance"]
        )

        conn.execute("""
            INSERT INTO performance
            (
                student_id,
                subject,
                marks,
                attendance
            )
            VALUES (?, ?, ?, ?)
        """, (
            student_id,
            subject,
            marks,
            attendance_value
        ))

        conn.commit()

    # -----------------------------------------------------
    # Get student's performance
    # -----------------------------------------------------

    performance = conn.execute("""
        SELECT *
        FROM performance
        WHERE student_id = ?
        ORDER BY id DESC
    """, (
        student_id,
    )).fetchall()

    conn.close()

    # =====================================================
    # AVERAGE MARKS
    # =====================================================

    if performance:

        average = sum(
            float(record["marks"])
            for record in performance
        ) / len(performance)

    else:

        average = 0

    # =====================================================
    # GRADE
    # =====================================================

    if average >= 90:

        grade = "A+"

    elif average >= 80:

        grade = "A"

    elif average >= 70:

        grade = "B"

    elif average >= 60:

        grade = "C"

    elif average >= 50:

        grade = "D"

    else:

        grade = "F"

    # =====================================================
    # ATTENDANCE
    # =====================================================

    if performance:

        attendance = sum(
            float(record["attendance"])
            for record in performance
        ) / len(performance)

    else:

        attendance = 0

    # =====================================================
    # RENDER PAGE
    # =====================================================

    return render_template(

        "student_performance.html",

        student=student,

        performance=performance,

        average=round(
            average,
            2
        ),

        grade=grade,

        attendance=round(
            attendance,
            2
        )
    )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )