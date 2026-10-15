
import re

from database import (
    add_student,
    view_students,
    search_student,
    search_by_department,
    search_by_name,
    search_by_email,
    search_by_roll_range,
    search_by_email_domain,
    search_by_department_and_domain,
    update_student,
    delete_student,
    get_statistics,
    get_department_report,
    sort_students,
    export_students_to_csv,
    import_students_from_csv,
    check_login,
    change_password
)


# -------------------- INPUT VALIDATION --------------------

def get_input(message):
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Input cannot be empty. Please try again.")


def valid_email(email):
    return re.fullmatch(
        r"[\w.-]+@[\w.-]+\.\w+",
        email
    ) is not None


def valid_roll_number(roll_no):
    return roll_no.isdigit()


def valid_email_domain(domain):
    return re.fullmatch(
        r"[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+",
        domain
    ) is not None


def get_valid_email():
    while True:
        email = get_input("Enter email: ")

        if valid_email(email):
            return email

        print("Invalid email. Example: student@gmail.com")


def get_valid_roll_number():
    while True:
        roll_no = get_input("Enter roll number: ")

        if valid_roll_number(roll_no):
            return roll_no

        print("Roll number must contain digits only.")


# -------------------- DISPLAY STUDENTS --------------------

def display_students(students):
    if not students:
        print("No students found.")
        return

    print("-" * 95)
    print(
        f"{'ID':<5}"
        f"{'Name':<22}"
        f"{'Roll No':<15}"
        f"{'Department':<20}"
        f"{'Email':<33}"
    )
    print("-" * 95)

    for student in students:
        student_id, name, roll_no, department, email = student

        print(
            f"{student_id:<5}"
            f"{name[:20]:<22}"
            f"{roll_no:<15}"
            f"{department[:18]:<20}"
            f"{email[:31]:<33}"
        )

    print("-" * 95)


# -------------------- LOGIN --------------------

def login():
    print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
    print("Please log in to continue.")

    for attempt in range(3):
        username = get_input("Username: ")
        password = input("Password: ")

        if check_login(username, password):
            print(f"\nWelcome, {username}!")
            return username

        remaining = 2 - attempt

        if remaining > 0:
            print(f"Invalid login. Attempts remaining: {remaining}")

    print("Too many failed attempts. Exiting.")
    return None


# -------------------- ADD STUDENT --------------------

def add_student_menu():
    name = get_input("Enter student name: ")
    roll_no = get_valid_roll_number()
    department = get_input("Enter department: ")
    email = get_valid_email()

    if add_student(name, roll_no, department, email):
        print("Student added successfully!")
    else:
        print("This roll number already exists.")


# -------------------- UPDATE STUDENT --------------------

def update_student_menu():
    roll_no = get_input("Enter roll number to update: ")
    student = search_student(roll_no)

    if not student:
        print("Student not found.")
        return

    print("Enter the new details.")

    name = get_input("New name: ")
    department = get_input("New department: ")
    email = get_valid_email()

    result = update_student(roll_no, name, department, email)

    if result:
        print("Student updated successfully!")
    else:
        print("Unable to update student.")


# -------------------- DELETE STUDENT --------------------

def delete_student_menu():
    roll_no = get_input("Enter roll number to delete: ")
    student = search_student(roll_no)

    if not student:
        print("Student not found.")
        return

    confirmation = input(
        f"Delete student {student[1]} ({roll_no})? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        if delete_student(roll_no):
            print("Student deleted successfully!")
        else:
            print("Unable to delete student.")
    else:
        print("Deletion cancelled.")


# -------------------- STATISTICS --------------------

def show_statistics():
    total_students, department_counts = get_statistics()

    print("\n========== STUDENT STATISTICS ==========")
    print(f"Total students: {total_students}")

    if not department_counts:
        print("No department records available.")
        return

    print("\nStudents by department:")

    for department, count in department_counts:
        print(f"{department}: {count}")


# -------------------- DEPARTMENT REPORT --------------------

def show_department_report():
    (
        total_students,
        department_counts,
        highest_departments,
        lowest_departments,
        average_students
    ) = get_department_report()

    print("\n========== DEPARTMENT REPORT ==========")
    print(f"Total students: {total_students}")

    if not department_counts:
        print("No student records available.")
        return

    print("\nDepartment-wise student count:")

    for department, count in department_counts:
        print(f"{department}: {count} students")

    print("\nHighest student count:")

    for department, count in highest_departments:
        print(f"{department}: {count} students")

    print("\nLowest student count:")

    for department, count in lowest_departments:
        print(f"{department}: {count} students")

    print(
        f"\nAverage students per department: "
        f"{average_students:.2f}"
    )


# -------------------- CHANGE PASSWORD --------------------

def update_password(username):
    old_password = input("Enter current password: ")
    new_password = input("Enter new password: ")

    if len(new_password) < 8:
        print("Password must contain at least 8 characters.")
        return

    if new_password == old_password:
        print("New password must be different from the old password.")
        return

    confirm_password = input("Confirm new password: ")

    if new_password != confirm_password:
        print("Passwords do not match.")
        return

    if change_password(username, old_password, new_password):
        print("Password changed successfully!")
    else:
        print("Current password is incorrect.")


# -------------------- MENU --------------------

def display_menu():
    print("\n========== MAIN MENU ==========")
    print("1.  Add Student")
    print("2.  View All Students")
    print("3.  Search by Roll Number")
    print("4.  Search by Name")
    print("5.  Update Student")
    print("6.  Delete Student")
    print("7.  Student Statistics")
    print("8.  Search by Department")
    print("9.  Sort Students")
    print("10. Export Students to CSV")
    print("11. Import Students from CSV")
    print("12. Change Password")
    print("13. Department Report")
    print("14. Search Student by Email")
    print("15. Search by Roll Number Range")
    print("16. Search by Email Domain")
    print("17. Search by Department and Email Domain")
    print("18. Exit")


# -------------------- MAIN PROGRAM --------------------

def main():
    username = login()

    if username is None:
        return

    while True:
        display_menu()
        choice = input("Enter your choice (1-18): ").strip()

        # 1. Add student
        if choice == "1":
            add_student_menu()

        # 2. View all students
        elif choice == "2":
            display_students(view_students())

        # 3. Search by roll number
        elif choice == "3":
            roll_no = get_input("Enter roll number: ")
            student = search_student(roll_no)

            if student:
                display_students([student])
            else:
                print("Student not found.")

        # 4. Search by name
        elif choice == "4":
            name = get_input("Enter student name: ")
            display_students(search_by_name(name))

        # 5. Update student
        elif choice == "5":
            update_student_menu()

        # 6. Delete student
        elif choice == "6":
            delete_student_menu()

        # 7. Student statistics
        elif choice == "7":
            show_statistics()

        # 8. Search by department
        elif choice == "8":
            department = get_input("Enter department: ")
            students = search_by_department(department)
            display_students(students)

        # 9. Sort students
        elif choice == "9":
            print("\n1. Sort by Name")
            print("2. Sort by Roll Number")
            print("3. Sort by Department")

            sort_option = input("Choose sorting option: ").strip()
            students = sort_students(sort_option)

            if students is None:
                print("Invalid sorting option.")
            else:
                display_students(students)

        # 10. Export students to CSV
        elif choice == "10":
            if export_students_to_csv():
                print("Students exported to students.csv successfully!")
            else:
                print("No students available to export.")

        # 11. Import students from CSV
        elif choice == "11":
            print("Place students.csv in your project folder first.")
            confirmation = input(
                "Do you want to import the file? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":
                imported, skipped = import_students_from_csv()

                if imported == -1:
                    print("students.csv was not found or is empty.")
                elif imported == -2:
                    print(
                        "CSV headers are incorrect. Required headers: "
                        "Name, Roll No, Department, Email"
                    )
                else:
                    print(f"Students imported: {imported}")
                    print(f"Rows skipped: {skipped}")
            else:
                print("Import cancelled.")

        # 12. Change password
        elif choice == "12":
            update_password(username)

        # 13. Department report
        elif choice == "13":
            show_department_report()

        # 14. Search by email
        elif choice == "14":
            email = get_valid_email()
            display_students(search_by_email(email))

        # 15. Search by roll number range
        elif choice == "15":
            start_roll = get_valid_roll_number()
            end_roll = get_valid_roll_number()

            if int(start_roll) > int(end_roll):
                print("Starting roll number must be less than or equal to ending roll number.")
            else:
                students = search_by_roll_range(
                    int(start_roll),
                    int(end_roll)
                )
                display_students(students)

        # 16. Search by email domain
        elif choice == "16":
            domain = get_input(
                "Enter email domain (example: gmail.com): "
            ).lower().lstrip("@")

            if not valid_email_domain(domain):
                print("Invalid domain. Example: gmail.com")
            else:
                students = search_by_email_domain(domain)
                display_students(students)

        # 17. Day 25: Search by department AND email domain
        elif choice == "17":
            department = get_input("Enter department: ")

            domain = get_input(
                "Enter email domain (example: gmail.com): "
            ).lower().lstrip("@")

            if not valid_email_domain(domain):
                print("Invalid domain. Example: gmail.com")
                continue

            students = search_by_department_and_domain(
                department,
                domain
            )

            if students:
                print(
                    f"\nStudents in {department} using "
                    f"{domain} email addresses:"
                )
                display_students(students)
            else:
                print("No matching students found.")

        # 18. Exit
        elif choice == "18":
            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 18.")


if __name__ == "__main__":
    main()
