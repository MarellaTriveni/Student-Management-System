from database import (
    check_login,
    change_password,
    add_student,
    view_students,
    search_student,
    search_by_department,
    search_by_name,
    update_student,
    delete_student,
    get_statistics,
    sort_students,
    export_students_to_csv,
    import_students_from_csv,
    get_department_report
)

import re


# -----------------------------
# INPUT VALIDATION
# -----------------------------

def get_input(message):
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Input cannot be empty. Please try again.")


def valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def valid_roll_number(roll_no):
    return roll_no.isdigit()


# -----------------------------
# DISPLAY STUDENTS
# -----------------------------

def display_students(students):

    if not students:
        print("\nNo students found.")
        return

    print("\n" + "=" * 75)
    print(
        f"{'ID':<5}"
        f"{'Name':<20}"
        f"{'Roll No':<12}"
        f"{'Department':<15}"
        f"{'Email':<25}"
    )
    print("=" * 75)

    for student in students:

        print(
            f"{student[0]:<5}"
            f"{student[1]:<20}"
            f"{student[2]:<12}"
            f"{student[3]:<15}"
            f"{student[4]:<25}"
        )

    print("=" * 75)


# -----------------------------
# LOGIN
# -----------------------------

def login():

    print("\n" + "=" * 40)
    print("       STUDENT MANAGEMENT SYSTEM")
    print("=" * 40)

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if check_login(username, password):

        print("\nLogin successful!")
        return username

    print("\nInvalid username or password.")
    return None


# -----------------------------
# CHANGE PASSWORD
# -----------------------------

def update_password(username):

    print("\n--- Change Password ---")

    old_password = input("Enter old password: ").strip()

    new_password = input("Enter new password: ").strip()

    if not new_password:
        print("New password cannot be empty.")
        return

    if len(new_password) < 4:
        print("Password must contain at least 4 characters.")
        return

    confirm_password = input(
        "Confirm new password: "
    ).strip()

    if new_password != confirm_password:

        print("Passwords do not match.")
        return

    result = change_password(
        username,
        old_password,
        new_password
    )

    if result:

        print("Password changed successfully!")

    else:

        print("Old password is incorrect.")


# -----------------------------
# DEPARTMENT REPORT
# -----------------------------

def show_department_report():

    print("\n" + "=" * 50)
    print("          DEPARTMENT REPORT")
    print("=" * 50)

    (
        total_students,
        department_counts,
        highest_department,
        lowest_department,
        average_students
    ) = get_department_report()

    print(
        f"\nTotal Students: {total_students}"
    )

    if not department_counts:

        print("No department data available.")
        return

    print("\nDepartment Summary:")

    for department, count in department_counts:

        print(
            f"{department} : {count} students"
        )

    print(
        f"\nHighest Student Department: "
        f"{highest_department[0]} - "
        f"{highest_department[1]} students"
    )

    print(
        f"Lowest Student Department: "
        f"{lowest_department[0]} - "
        f"{lowest_department[1]} students"
    )

    print(
        f"Average Students per Department: "
        f"{average_students:.1f}"
    )

    print("=" * 50)


# -----------------------------
# MAIN MENU
# -----------------------------

def main():

    current_user = login()

    if current_user is None:
        return

    while True:

        print("\n" + "=" * 50)
        print("          STUDENT MANAGEMENT SYSTEM")
        print("=" * 50)

        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by Roll Number")
        print("4. Search Student by Name")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Student Statistics")
        print("8. Search by Department")
        print("9. Sort Students")
        print("10. Export Students to CSV")
        print("11. Import Students from CSV")
        print("12. Change Password")
        print("13. Department Report")
        print("14. Exit")

        print("=" * 50)

        choice = input(
            "Enter your choice: "
        ).strip()

        # -------------------------
        # ADD STUDENT
        # -------------------------

        if choice == "1":

            print("\n--- Add Student ---")

            name = get_input("Enter name: ")

            roll_no = get_input(
                "Enter roll number: "
            )

            if not valid_roll_number(roll_no):

                print(
                    "Roll number must contain only numbers."
                )
                continue

            department = get_input(
                "Enter department: "
            )

            email = get_input(
                "Enter email: "
            )

            if not valid_email(email):

                print("Invalid email format.")
                continue

            result = add_student(
                name,
                roll_no,
                department,
                email
            )

            if result:

                print(
                    "\nStudent added successfully!"
                )

            else:

                print(
                    "\nRoll number already exists."
                )

        # -------------------------
        # VIEW STUDENTS
        # -------------------------

        elif choice == "2":

            students = view_students()

            display_students(students)

        # -------------------------
        # SEARCH BY ROLL NUMBER
        # -------------------------

        elif choice == "3":

            roll_no = get_input(
                "Enter roll number: "
            )

            student = search_student(roll_no)

            if student:

                print("\nStudent Found!")

                print(
                    f"ID: {student[0]}"
                )
                print(
                    f"Name: {student[1]}"
                )
                print(
                    f"Roll No: {student[2]}"
                )
                print(
                    f"Department: {student[3]}"
                )
                print(
                    f"Email: {student[4]}"
                )

            else:

                print("\nStudent not found.")

        # -------------------------
        # SEARCH BY NAME
        # -------------------------

        elif choice == "4":

            name = get_input(
                "Enter student name: "
            )

            students = search_by_name(name)

            display_students(students)

        # -------------------------
        # UPDATE STUDENT
        # -------------------------

        elif choice == "5":

            print("\n--- Update Student ---")

            roll_no = get_input(
                "Enter roll number: "
            )

            student = search_student(roll_no)

            if not student:

                print("Student not found.")
                continue

            name = get_input(
                "Enter new name: "
            )

            department = get_input(
                "Enter new department: "
            )

            email = get_input(
                "Enter new email: "
            )

            if not valid_email(email):

                print("Invalid email format.")
                continue

            result = update_student(
                roll_no,
                name,
                department,
                email
            )

            if result:

                print(
                    "Student updated successfully!"
                )

            else:

                print("Update failed.")

        # -------------------------
        # DELETE STUDENT
        # -------------------------

        elif choice == "6":

            roll_no = get_input(
                "Enter roll number: "
            )

            student = search_student(roll_no)

            if not student:

                print("Student not found.")
                continue

            confirm = input(
                "Are you sure you want to delete? (y/n): "
            ).strip().lower()

            if confirm == "y":

                result = delete_student(roll_no)

                if result:

                    print(
                        "Student deleted successfully!"
                    )

                else:

                    print("Delete failed.")

            else:

                print("Delete cancelled.")

        # -------------------------
        # STATISTICS
        # -------------------------

        elif choice == "7":

            total_students, department_counts = (
                get_statistics()
            )

            print("\n--- Student Statistics ---")

            print(
                f"Total Students: {total_students}"
            )

            print("\nDepartment-wise Students:")

            for department, count in department_counts:

                print(
                    f"{department}: {count}"
                )

        # -------------------------
        # SEARCH BY DEPARTMENT
        # -------------------------

        elif choice == "8":

            department = get_input(
                "Enter department: "
            )

            students = search_by_department(
                department
            )

            display_students(students)

        # -------------------------
        # SORT STUDENTS
        # -------------------------

        elif choice == "9":

            print("\n--- Sort Students ---")

            print("1. Sort by Name")
            print("2. Sort by Roll Number")
            print("3. Sort by Department")

            sort_option = input(
                "Enter your choice: "
            ).strip()

            students = sort_students(
                sort_option
            )

            if students:

                display_students(students)

            else:

                print("Invalid sorting option.")

        # -------------------------
        # EXPORT CSV
        # -------------------------

        elif choice == "10":

            result = export_students_to_csv()

            if result:

                print(
                    "\nStudents exported successfully!"
                )
                print(
                    "File created: students.csv"
                )

            else:

                print(
                    "\nNo students available to export."
                )

        # -------------------------
        # IMPORT CSV
        # -------------------------

        elif choice == "11":

            imported, skipped = (
                import_students_from_csv()
            )

            if imported == -1:

                print(
                    "\nstudents.csv file not found."
                )

            else:

                print(
                    f"\nImported Students: {imported}"
                )

                print(
                    f"Skipped Students: {skipped}"
                )

        # -------------------------
        # CHANGE PASSWORD
        # -------------------------

        elif choice == "12":

            update_password(current_user)

        # -------------------------
        # DEPARTMENT REPORT
        # -------------------------

        elif choice == "13":

            show_department_report()

        # -------------------------
        # EXIT
        # -------------------------

        elif choice == "14":

            print(
                "\nThank you for using "
                "Student Management System!"
            )

            break

        else:

            print(
                "\nInvalid choice. Please try again."
            )


# -----------------------------
# START PROGRAM
# -----------------------------

if __name__ == "__main__":
    main()