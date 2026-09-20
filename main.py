import sqlite3


class Student:
    def __init__(self, name, roll_no, department, email):
        self.name = name
        self.roll_no = roll_no
        self.department = department
        self.email = email

    def display_details(self):
        print("----- Student Details -----")
        print("Name:", self.name)
        print("Roll No:", self.roll_no)
        print("Department:", self.department)
        print("Email:", self.email)
        print("---------------------------")


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


# Create database
create_database()

print("Student Management System")
print("Database is ready!")