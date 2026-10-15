
import sqlite3
import csv
import hashlib


# -------------------- PASSWORD SECURITY --------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------- DATABASE SETUP --------------------

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

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", hash_password("admin123"))
        )

    connection.commit()
    connection.close()


def migrate_existing_passwords():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, password FROM users")
    users = cursor.fetchall()

    for user_id, password in users:
        # Convert older plain-text passwords to SHA-256 hashes.
        if len(password) != 64 or any(
            character not in "0123456789abcdefABCDEF"
            for character in password
        ):
            cursor.execute(
                "UPDATE users SET password = ? WHERE id = ?",
                (hash_password(password), user_id)
            )

    connection.commit()
    connection.close()


# -------------------- LOGIN --------------------

def check_login(username, password):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()
    connection.close()

    return result is not None and result[0] == hash_password(password)


def change_password(username, old_password, new_password):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()

    if result is None or result[0] != hash_password(old_password):
        connection.close()
        return False

    cursor.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (hash_password(new_password), username)
    )

    connection.commit()
    connection.close()
    return True


# -------------------- ADD STUDENT --------------------

def add_student(name, roll_no, department, email):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (name, roll_no, department, email)
            VALUES (?, ?, ?, ?)
        """, (name, roll_no, department, email))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


# -------------------- VIEW STUDENTS --------------------

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


# -------------------- SEARCH BY ROLL NUMBER --------------------

def search_student(roll_no):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        WHERE roll_no = ?
    """, (roll_no,))

    student = cursor.fetchone()
    connection.close()
    return student


# -------------------- SEARCH BY DEPARTMENT --------------------

def search_by_department(department):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        WHERE LOWER(department) = LOWER(?)
        ORDER BY name ASC
    """, (department.strip(),))

    students = cursor.fetchall()
    connection.close()
    return students


# -------------------- SEARCH BY NAME --------------------

def search_by_name(name):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        WHERE LOWER(name) LIKE LOWER(?)
        ORDER BY name ASC
    """, ("%" + name.strip() + "%",))

    students = cursor.fetchall()
    connection.close()
    return students


# -------------------- SEARCH BY EMAIL --------------------

def search_by_email(email):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        WHERE LOWER(email) = LOWER(?)
    """, (email.strip(),))

    students = cursor.fetchall()
    connection.close()
    return students


# -------------------- SEARCH BY ROLL NUMBER RANGE --------------------

def search_by_roll_range(start_roll, end_roll):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        WHERE roll_no NOT GLOB '*[^0-9]*'
          AND CAST(roll_no AS INTEGER) BETWEEN ? AND ?
        ORDER BY CAST(roll_no AS INTEGER) ASC
    """, (start_roll, end_roll))

    students = cursor.fetchall()
    connection.close()
    return students


# -------------------- SEARCH BY EMAIL DOMAIN --------------------

def search_by_email_domain(domain):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    domain = domain.strip().lower().lstrip("@")

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        WHERE LOWER(email) LIKE ?
        ORDER BY name ASC
    """, ("%@" + domain,))

    students = cursor.fetchall()
    connection.close()
    return students


# -------------------- DAY 25: DEPARTMENT + EMAIL DOMAIN --------------------

def search_by_department_and_domain(department, domain):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    department = department.strip()
    domain = domain.strip().lower().lstrip("@")

    cursor.execute("""
        SELECT id, name, roll_no, department, email
        FROM students
        WHERE LOWER(department) = LOWER(?)
          AND LOWER(email) LIKE ?
        ORDER BY name ASC
    """, (department, "%@" + domain))

    students = cursor.fetchall()
    connection.close()
    return students


# -------------------- UPDATE STUDENT --------------------

def update_student(roll_no, name, department, email):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?, department = ?, email = ?
        WHERE roll_no = ?
    """, (name, department, email, roll_no))

    updated_count = cursor.rowcount
    connection.commit()
    connection.close()
    return updated_count


# -------------------- DELETE STUDENT --------------------

def delete_student(roll_no):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    deleted_count = cursor.rowcount
    connection.commit()
    connection.close()
    return deleted_count


# -------------------- STATISTICS --------------------

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


# -------------------- DEPARTMENT REPORT --------------------

def get_department_report():
    total_students, department_counts = get_statistics()

    if not department_counts:
        return total_students, [], [], [], 0

    highest_count = max(count for _, count in department_counts)
    lowest_count = min(count for _, count in department_counts)

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

    average_students = total_students / len(department_counts)

    return (
        total_students,
        department_counts,
        highest_departments,
        lowest_departments,
        average_students
    )


# -------------------- SORT STUDENTS --------------------

def sort_students(sort_option):
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    if sort_option == "1":
        order_by = "name COLLATE NOCASE ASC"
    elif sort_option == "2":
        order_by = "CAST(roll_no AS INTEGER) ASC"
    elif sort_option == "3":
        order_by = "department COLLATE NOCASE ASC"
    else:
        connection.close()
        return None

    cursor.execute(f"""
        SELECT id, name, roll_no, department, email
        FROM students
        ORDER BY {order_by}
    """)

    students = cursor.fetchall()
    connection.close()
    return students


# -------------------- EXPORT TO CSV --------------------

def export_students_to_csv():
    students = view_students()

    if not students:
        return False

    with open("students.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Roll No", "Department", "Email"])
        writer.writerows(students)

    return True


# -------------------- IMPORT FROM CSV --------------------

def import_students_from_csv():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    imported_count = 0
    skipped_count = 0

    try:
        with open("students.csv", "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            required_columns = {"Name", "Roll No", "Department", "Email"}

            if not reader.fieldnames:
                return -1, 0

            if not required_columns.issubset(set(reader.fieldnames)):
                return -2, 0

            for row in reader:
                name = (row.get("Name") or "").strip()
                roll_no = (row.get("Roll No") or "").strip()
                department = (row.get("Department") or "").strip()
                email = (row.get("Email") or "").strip()

                if not all([name, roll_no, department, email]):
                    skipped_count += 1
                    continue

                try:
                    cursor.execute("""
                        INSERT INTO students (name, roll_no, department, email)
                        VALUES (?, ?, ?, ?)
                    """, (name, roll_no, department, email))

                    imported_count += 1

                except sqlite3.IntegrityError:
                    skipped_count += 1

        connection.commit()
        return imported_count, skipped_count

    except FileNotFoundError:
        return -1, 0

    finally:
        connection.close()


# Create database and migrate older passwords when this module loads.
create_database()
migrate_existing_passwords()
