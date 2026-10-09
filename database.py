import sqlite3
import csv


# Create database and tables
def create_database():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create default admin account
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",)
    )

    user = cursor.fetchone()

    if user is None:
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, ("admin", "admin123"))

    connection.commit()
    connection.close()


# Login check
def check_login(username, password):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    connection.close()

    return user is not None


# Change password
def change_password(username, old_password, new_password):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (username, old_password))

    user = cursor.fetchone()

    if user is None:
        connection.close()
        return False

    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE username = ?
    """, (new_password, username))

    connection.commit()
    connection.close()

    return True


# Add student
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


# View all students
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


# Search student by roll number
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


# Search by department
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


# Search by name
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


# Update student
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


# Delete student
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


# Student statistics
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


# Day 20 - Department Report
def get_department_report():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    # Total students
    cursor.execute("SELECT COUNT(*) FROM students")

    total_students = cursor.fetchone()[0]

    # Students in each department
    cursor.execute("""
        SELECT department, COUNT(*)
        FROM students
        GROUP BY department
        ORDER BY COUNT(*) DESC
    """)

    department_counts = cursor.fetchall()

    connection.close()

    # No students
    if not department_counts:
        return (
            total_students,
            [],
            None,
            None,
            0
        )

    # Highest student department
    highest_department = department_counts[0]

    # Lowest student department
    lowest_department = department_counts[-1]

    # Average students per department
    average_students = (
        total_students /
        len(department_counts)
    )

    return (
        total_students,
        department_counts,
        highest_department,
        lowest_department,
        average_students
    )


# Sort students
def sort_students(sort_option):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    if sort_option == "1":

        # Sort by name
        cursor.execute("""
            SELECT id, name, roll_no, department, email
            FROM students
            ORDER BY name ASC
        """)

    elif sort_option == "2":

        # Sort by roll number
        cursor.execute("""
            SELECT id, name, roll_no, department, email
            FROM students
            ORDER BY CAST(roll_no AS INTEGER) ASC
        """)

    elif sort_option == "3":

        # Sort by department
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


# Export students to CSV
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

    if not students:
        return False

    with open(
        "students.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Name",
            "Roll No",
            "Department",
            "Email"
        ])

        writer.writerows(students)

    return True


# Import students from CSV
def import_students_from_csv():

    try:
        with open(
            "students.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            connection = sqlite3.connect("student.db")
            cursor = connection.cursor()

            imported_count = 0
            skipped_count = 0

            for row in reader:

                name = row["Name"].strip()
                roll_no = row["Roll No"].strip()
                department = row["Department"].strip()
                email = row["Email"].strip()

                try:

                    cursor.execute("""
                        INSERT INTO students
                        (name, roll_no, department, email)
                        VALUES (?, ?, ?, ?)
                    """, (
                        name,
                        roll_no,
                        department,
                        email
                    ))

                    imported_count += 1

                except sqlite3.IntegrityError:

                    skipped_count += 1

            connection.commit()
            connection.close()

            return (
                imported_count,
                skipped_count
            )

    except FileNotFoundError:

        return -1, 0


# Create database
create_database()