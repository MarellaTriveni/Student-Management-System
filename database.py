import sqlite3


def create_database():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_student(name, roll_no, department, email):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students (name, roll_no, department, email)
        VALUES (?, ?, ?, ?)
    """, (name, roll_no, department, email))

    connection.commit()
    connection.close()

    print("Student added successfully!")


def view_students():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    connection.close()

    return students


def search_student(roll_no):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    connection.close()

    return student


def update_student(roll_no, name, department, email):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?, department = ?, email = ?
        WHERE roll_no = ?
    """, (name, department, email, roll_no))

    connection.commit()

    rows_updated = cursor.rowcount

    connection.close()

    return rows_updated


create_database()