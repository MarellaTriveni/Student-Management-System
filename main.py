
import re

from database import (
    check_login,
    change_password,
    add_student,
    view_students,
    search_student,
    search_by_department,
    search_by_name,
    search_by_email,
    search_by_roll_range,
    update_student,
    delete_student,
    get_statistics,
    sort_students,
    export_students_to_csv,
    import_students_from_csv,
    get_department_report
)


# =====================================
# INPUT VALIDATION
# =====================================

def get_input(message):
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Input cannot be empty. Try again.")


def valid_email(email):
    pattern = r"^[\w.-]+@[\w.-]+\.\w+$"
    return re.fullmatch(pattern, email) is not None


def valid_roll_number(roll_no):
    return roll_no.isdigit()


# =====================================
# DISPLAY STUDENTS
# =====================================

def display_students(students):
    if not students:
        print("\nNo students found.")
        return

    print("\n" + "=" * 100)
    print(
        f"{'ID':<5}"
        f"{'Name':<20}"
        f"{'Roll No':<15}"
        f"{'Department':<15}"
        f"{'Email':<40}"
    )
    print("=" * 100)

    for student in students:
        print(
            f"{student[0]:<5}"
            f"{student[1][:19]:<20}"
            f"{student[2][:14]:<15}"
            f"{student[3][:14]:<15}"
            f"{student[4][:39]:<40}"
        )

    print("=" * 100)


# =====================================
# LOGIN
# =====================================

def login():
    print("\n" + "=" * 40)
    print("   STUDENT MANAGEMENT SYSTEM")
    print("=" * 40)

    for attempt in range(3):
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if check_login(username, password):
            print("\nLogin successful!")
            return username

        remaining = 2 - attempt

        if remaining > 0:
            print(
                f"Invalid login. Attempts remaining: {remaining}"
            )

    print("Too many failed attempts.")
    return None


# =====================================
# CHANGE PASSWORD
# =====================================

def update_password(username):
    print("\n--- Change Password ---")

    old_password = input(
        "Enter current password: "
    ).strip()

    new_password = input(
        "Enter new password: "
    ).strip()

    if len(new_password) < 8:
        print("Password must be at least 8 characters.")
        return

    if new_password == old_password:
        print("Choose a different password.")
        return

    confirm_password = input(
        "Confirm new password: "
    ).strip()

    if new_password != confirm_password:
        print("Passwords do not match.")
        return

    if change_password(
        username, old_password, new_password
    ):
        print("Password changed successfully!")
    else:
        print("Current password is incorrect.")


# =====================================
# DEPARTMENT REPORT
# =====================================

def show_department_report():
    print("\n--- Department Report ---")

    (
        total_students,
        department_counts,
        highest_departments,
        lowest_departments,
        average_students
    ) = get_department_report()

    print(f"Total Students: {total_students}")

    if not department_counts:
        print("No department data available.")
        return

    print("\nDepartment-wise Count:")

    for department, count in department_counts:
        print(f"{department}: {count} students")

    print("\nDepartment(s) with the most students:")

    for department, count in highest_departments:
        print(f"{department}: {count} students")

    print("\nDepartment(s) with the fewest students:")

    for department, count in lowest_departments:
        print(f"{department}: {count} students")

    print(
        f"\nAverage students per department: "
        f"{average_students:.1f}"
    )


# =====================================
# MAIN PROGRAM
# =====================================

def main():
    current_user = login()

    if current_user is None:
        return

    while True:
        print("\n" + "=" * 45)
        print("      STUDENT MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Add Student")
        print("2. View All Students")
        print("3. Search by Roll Number")
        print("4. Search by Name")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Student Statistics")
        print("8. Search by Department")
        print("9. Sort Students")
        print("10. Export Students to CSV")
        print("11. Import Students from CSV")
        print("12. Change Password")
        print("13. Department Report")
        print("14. Search Student by Email")
        print("15. Search Students by Roll Number Range")
        print("16. Exit")

        print("=" * 45)

        choice = input("Enter your choice: ").strip()

        # 1. ADD STUDENT
        if choice == "1":
            print("\n--- Add Student ---")

            name = get_input("Enter name: ")
            roll_no = get_input("Enter roll number: ")

            if not valid_roll_number(roll_no):
                print("Roll number must contain digits only.")
                continue

            department = get_input("Enter department: ")
            email = get_input("Enter email: ")

            if not valid_email(email):
                print("Invalid email format.")
                continue

            if add_student(name, roll_no, department, email):
                print("Student added successfully!")
            else:
                print("This roll number already exists.")

        # 2. VIEW ALL STUDENTS
        elif choice == "2":
            display_students(view_students())

        # 3. SEARCH BY ROLL NUMBER
        elif choice == "3":
            roll_no = get_input("Enter roll number: ")
            student = search_student(roll_no)

            if student:
                display_students([student])
            else:
                print("Student not found.")

        # 4. SEARCH BY NAME
        elif choice == "4":
            name = get_input("Enter student name: ")
            display_students(search_by_name(name))

        # 5. UPDATE STUDENT
        elif choice == "5":
            roll_no = get_input("Enter roll number to update: ")
            student = search_student(roll_no)

            if not student:
                print("Student not found.")
                continue

            name = get_input("Enter new name: ")
            department = get_input("Enter new department: ")
            email = get_input("Enter new email: ")

            if not valid_email(email):
                print("Invalid email format.")
                continue

            result = update_student(
                roll_no, name, department, email
            )

            if result:
                print("Student updated successfully!")
            else:
                print("No changes were made.")

        # 6. DELETE STUDENT
        elif choice == "6":
            roll_no = get_input("Enter roll number to delete: ")
            student = search_student(roll_no)

            if not student:
                print("Student not found.")
                continue

            confirm = input(
                "Delete this student? (y/n): "
            ).strip().lower()

            if confirm == "y":
                if delete_student(roll_no):
                    print("Student deleted successfully!")
                else:
                    print("Unable to delete student.")
            else:
                print("Delete cancelled.")

        # 7. STUDENT STATISTICS
        elif choice == "7":
            total, departments = get_statistics()

            print("\n--- Student Statistics ---")
            print(f"Total Students: {total}")
            print("\nDepartment-wise Count:")

            if departments:
                for department, count in departments:
                    print(f"{department}: {count}")
            else:
                print("No student records available.")

        # 8. SEARCH BY DEPARTMENT
        elif choice == "8":
            department = get_input("Enter department: ")
            display_students(
                search_by_department(department)
            )

        # 9. SORT STUDENTS
        elif choice == "9":
            print("\n1. Sort by Name")
            print("2. Sort by Roll Number")
            print("3. Sort by Department")

            sort_option = input(
                "Choose sorting option: "
            ).strip()

            students = sort_students(sort_option)

            if students is None:
                print("Invalid sorting option.")
            else:
                display_students(students)

        # 10. EXPORT TO CSV
        elif choice == "10":
            if export_students_to_csv():
                print("Students exported to students.csv")
            else:
                print("No students available to export.")

        # 11. IMPORT FROM CSV
        elif choice == "11":
            imported, skipped = import_students_from_csv()

            if imported == -1:
                print("students.csv file not found.")
            elif imported == -2:
                print("CSV file has incorrect column headings.")
            else:
                print(f"Students imported: {imported}")
                print(f"Rows skipped: {skipped}")

        # 12. CHANGE PASSWORD
        elif choice == "12":
            update_password(current_user)

        # 13. DEPARTMENT REPORT
        elif choice == "13":
            show_department_report()

        # 14. SEARCH BY EMAIL
        elif choice == "14":
            email = get_input("Enter student email: ")

            if not valid_email(email):
                print("Please enter a valid email address.")
                continue

            student = search_by_email(email)

            if student:
                print("\nStudent found!")
                display_students([student])
            else:
                print("No student found with this email.")

        # 15. DAY 23: SEARCH BY ROLL NUMBER RANGE
        elif choice == "15":
            try:
                start_roll = int(
                    get_input("Enter starting roll number: ")
                )

                end_roll = int(
                    get_input("Enter ending roll number: ")
                )

                if start_roll < 0 or end_roll < 0:
                    print("Roll numbers cannot be negative.")

                elif start_roll > end_roll:
                    print(
                        "Starting roll number must be "
                        "less than or equal to ending roll number."
                    )

                else:
                    students = search_by_roll_range(
                        start_roll, end_roll
                    )

                    print(
                        f"\nStudents with roll numbers "
                        f"between {start_roll} and {end_roll}:"
                    )

                    display_students(students)

            except ValueError:
                print("Please enter valid numeric roll numbers.")

        # 16. EXIT
        elif choice == "16":
            print(
                "Thank you for using Student Management System!"
            )
            break

        else:
            print("Invalid choice. Enter a number from 1 to 16.")


# =====================================
# RUN PROGRAM
# =====================================

if __name__ == "__main__":
    main()
