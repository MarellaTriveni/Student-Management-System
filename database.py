
import sqlite3
import csv
import hashlib


# =====================================
# DAY 21: PASSWORD HASHING
# =====================================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =====================================
# CREATE DATABASE
# =====================================

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        ("admin",)
    )

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, ("admin", hash_password("admin123")))

    connection.commit()
    connection.close()


# =====================================
# MIGRATE OLD PASSWORDS
# =====================================

def migrate_existing_passwords():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, password FROM users")
    users = cursor.fetchall()

    for user_id, password in users:
        is_sha256 = (
            len(password) == 64
            and all(
                character in "0123456789abcdefABCDEF"
                for character in password
            )
        )

        if not is_sha256:
            cursor.execute("""
                UPDATE users
                SET password = ?
                WHERE id = ?
            """, (hash_password(password), user_id))

    connection.commit()
    connection.close()


# =====================================
# LOGIN
# =====================================

def check_login(username, password):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT password FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    connection.close()

    if user is None:
        return False

    return user[0] == hash_password(password)


# =====================================
# CHANGE PASSWORD
# =====================================

def change_password(username, old_password, new_password):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT password FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    if user is None:
        connection.close()
        return False

    if user[0] != hash_password(old_password):
        connection.close()
        return False

    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE username = ?
    """, (hash_password(new_password), username))

    connection.commit()
    connection.close()
    return True


# =====================================
# ADD STUDENT
# =====================================

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


# =====================================
# VIEW STUDENTS
# =====================================

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


# =====================================
# SEARCH BY ROLL NUMBER
# =====================================

def search_student(roll_no):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE roll_no = ?
    """, (roll_no,))

    student = cursor.fetchone()
    connection.close()
    return student


# =====================================
# SEARCH BY DEPARTMENT
# =====================================

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


# =====================================
# SEARCH BY NAME
# =====================================

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


# =====================================
# UPDATE STUDENT
# =====================================

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


# =====================================
# DELETE STUDENT
# =====================================

def delete_student(roll_no):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM students
        WHERE roll_no = ?
    """, (roll_no,))

    connection.commit()
    rows_deleted = cursor.rowcount
    connection.close()
    return rows_deleted


# =====================================
# STUDENT STATISTICS
# =====================================

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


# =====================================
# DAY 20: DEPARTMENT REPORT
# =====================================

def get_department_report():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("""
        SELECT department, COUNT(*)
        FROM students
        GROUP BY department
        ORDER BY department ASC
    """)

    department_counts = cursor.fetchall()
    connection.close()

    if not department_counts:
        return total_students, [], [], [], 0

    highest_count = max(
        count for _, count in department_counts
    )
    lowest_count = min(
        count for _, count in department_counts
    )

    highest_departments = [
        (department, count)
        for department, count in department_counts
        if count == highest_count
    ]

    lowest_departments = [
        (department, count)
        for department, count in department_counts
        if count == lowest_count
    ]

    average_students = (
        total_students / len(department_counts)
    )

    return (
        total_students,
        department_counts,
        highest_departments,
        lowest_departments,
        average_students
    )


# =====================================
# SORT STUDENTS
# =====================================

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
        return None

    students = cursor.fetchall()
    connection.close()
    return students


# =====================================
# EXPORT STUDENTS TO CSV
# =====================================

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
            "ID", "Name", "Roll No",
            "Department", "Email"
        ])

        writer.writerows(students)

    return True


# =====================================
# IMPORT STUDENTS FROM CSV
# =====================================

def import_students_from_csv():
    try:
        with open(
            "students.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)

            required_columns = {
                "Name", "Roll No", "Department", "Email"
            }

            if not reader.fieldnames or not required_columns.issubset(
                reader.fieldnames
            ):
                return -2, 0

            connection = sqlite3.connect("student.db")
            cursor = connection.cursor()

            imported_count = 0
            skipped_count = 0

            try:
                for row in reader:
                    name = (row.get("Name") or "").strip()
                    roll_no = (row.get("Roll No") or "").strip()
                    department = (
                        row.get("Department") or ""
                    ).strip()
                    email = (row.get("Email") or "").strip()

                    if not all([name, roll_no, department, email]):
                        skipped_count += 1
                        continue

                    try:
                        cursor.execute("""
                            INSERT INTO students
                            (name, roll_no, department, email)
                            VALUES (?, ?, ?, ?)
                        """, (
                            name, roll_no, department, email
                        ))

                        imported_count += 1

                    except sqlite3.IntegrityError:
                        skipped_count += 1

                connection.commit()

            finally:
                connection.close()

            return imported_count, skipped_count

    except FileNotFoundError:
        return -1, 0


# =====================================
# INITIALIZE DATABASE
# =====================================

create_database()
migrate_existing_passwords()
