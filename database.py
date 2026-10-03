import sqlite3
import csv


# --------------------------------
# CREATE DATABASE
# --------------------------------

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


# --------------------------------
# ADD STUDENT
# --------------------------------

def add_student(name, roll_no, department, email):

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO students
            (name, roll_no, department, email)
            VALUES (?, ?, ?, ?)
        """, (name, roll_no, department, email))

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


# --------------------------------
# VIEW STUDENTS
# --------------------------------

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


# --------------------------------
# SEARCH BY ROLL NUMBER
# --------------------------------

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


# --------------------------------
# SEARCH BY DEPARTMENT
# --------------------------------

def search_by_department(department):

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        WHERE LOWER(department) = LOWER(?)
        ORDER BY name ASC
    """, (department,))

    students = cursor.fetchall()

    connection.close()

    return students


# --------------------------------
# SEARCH BY NAME
# --------------------------------

def search_by_name(name):

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        WHERE LOWER(name) LIKE LOWER(?)
        ORDER BY name ASC
    """, ("%" + name + "%",))

    students = cursor.fetchall()

    connection.close()

    return students


# --------------------------------
# UPDATE STUDENT
# --------------------------------

def update_student(roll_no, name, department, email):

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?,
            department = ?,
            email = ?
        WHERE roll_no = ?
    """, (name, department, email, roll_no))

    connection.commit()

    rows_updated = cursor.rowcount

    connection.close()

    return rows_updated


# --------------------------------
# DELETE STUDENT
# --------------------------------

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


# --------------------------------
# STUDENT STATISTICS
# --------------------------------

def get_statistics():

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    total_students = cursor.fetchone()[0]

    cursor.execute("""
        SELECT department, COUNT(*)
        FROM students
        GROUP BY department
        ORDER BY department
    """)

    department_counts = cursor.fetchall()

    connection.close()

    return total_students, department_counts


# --------------------------------
# SORT STUDENTS
# --------------------------------

def sort_students(sort_option):

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    if sort_option == "1":

        cursor.execute("""
            SELECT id, name, roll_no, department, email
            FROM students
            ORDER BY name ASC
        """)

    elif sort_option == "2":

        cursor.execute("""
            SELECT id, name, roll_no, department, email
            FROM students
            ORDER BY CAST(roll_no AS INTEGER) ASC
        """)

    elif sort_option == "3":

        cursor.execute("""
            SELECT id, name, roll_no, department, email
            FROM students
            ORDER BY department ASC, name ASC
        """)

    else:

        connection.close()
        return []

    students = cursor.fetchall()

    connection.close()

    return students


# --------------------------------
# DAY 15 - EXPORT STUDENTS TO CSV
# --------------------------------

def export_students_to_csv():

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        ORDER BY name ASC
    """)

    students = cursor.fetchall()

    connection.close()

    # No students available
    if not students:

        return False

    # Create CSV file
    with open(
        "students.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # CSV headings
        writer.writerow([
            "ID",
            "Name",
            "Roll No",
            "Department",
            "Email"
        ])

        # Student data
        writer.writerows(students)

    return True


# --------------------------------
# CREATE DATABASE
# --------------------------------

create_database()