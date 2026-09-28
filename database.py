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


# Add Student
def add_student(name, roll_no, department, email):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (name, roll_no, department, email)
            VALUES (?, ?, ?, ?)
        """, (name, roll_no, department, email))

        connection.commit()
        print("\nStudent added successfully!")

    except sqlite3.IntegrityError:
        print("\nRoll Number already exists!")

    finally:
        connection.close()


# View All Students
def view_students():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        ORDER BY name ASC
    """)

    students = cursor.fetchall()

    connection.close()

    return students


# Search Student
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


# Update Student
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


# Delete Student
def delete_student(roll_no):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    connection.commit()

    rows_deleted = cursor.rowcount

    connection.close()

    return rows_deleted


# Student Statistics
def get_statistics():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    # Total students
    cursor.execute("SELECT COUNT(*) FROM students")

    total_students = cursor.fetchone()[0]

    # Department-wise students
    cursor.execute("""
        SELECT department, COUNT(*)
        FROM students
        GROUP BY department
        ORDER BY department
    """)

    department_counts = cursor.fetchall()

    connection.close()

    return total_students, department_counts


# Create database when program starts
create_database()