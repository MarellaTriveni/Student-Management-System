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


create_database()