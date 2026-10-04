import re

from database import (
    add_student,
    view_students,
    search_student,
    search_by_name,
    update_student,
    delete_student,
    get_statistics,
    search_by_department,
    sort_students,
    export_students_to_csv,
    import_students_from_csv
)


print("========================================")
print("      STUDENT MANAGEMENT SYSTEM")
print("========================================")


# --------------------------------
# GET REQUIRED INPUT
# --------------------------------

def get_input(message):

    while True:

        value = input(message).strip()

        if value != "":
            return value

        print("Input cannot be empty. Please try again.")


# --------------------------------
# VALIDATE EMAIL
# --------------------------------

def valid_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern, email) is not None


# --------------------------------
# VALIDATE ROLL NUMBER
# --------------------------------

def valid_roll_number(roll_no):

    return roll_no.isdigit()


# --------------------------------
# DISPLAY STUDENTS
# --------------------------------

def display_students(students):

    if not students:

        print("\nNo students found.")

        return

    for student in students:

        print("\nID:", student[0])
        print("Name:", student[1])
        print("Roll No:", student[2])
        print("Department:", student[3])
        print("Email:", student[4])

        print("----------------------------")


# --------------------------------
# MAIN MENU
# --------------------------------

while True:

    print("\n========== MENU ==========")

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
    print("12. Exit")

    print("==========================")

    choice = input("Enter your choice: ").strip()


    # ========================================
    # 1. ADD STUDENT
    # ========================================

    if choice == "1":

        print("\n========== ADD STUDENT ==========")

        name = get_input("Enter Student Name: ")

        roll_no = get_input("Enter Roll Number: ")

        if not valid_roll_number(roll_no):

            print("\nRoll Number must contain only numbers.")

            continue

        department = get_input(
            "Enter Department: "
        )

        email = get_input(
            "Enter Email: "
        )

        if not valid_email(email):

            print("\nInvalid email format.")

            print("Example: student@gmail.com")

            continue

        result = add_student(
            name,
            roll_no,
            department,
            email
        )

        if result:

            print("\nStudent added successfully! ✅")

        else:

            print("\nRoll Number already exists! ❌")


    # ========================================
    # 2. VIEW ALL STUDENTS
    # ========================================

    elif choice == "2":

        print("\n========== ALL STUDENTS ==========")

        students = view_students()

        display_students(students)


    # ========================================
    # 3. SEARCH BY ROLL NUMBER
    # ========================================

    elif choice == "3":

        print("\n========== SEARCH STUDENT ==========")

        roll_no = get_input(
            "Enter Roll Number: "
        )

        student = search_student(roll_no)

        if student:

            print("\nStudent Found! ✅")

            print("ID:", student[0])
            print("Name:", student[1])
            print("Roll No:", student[2])
            print("Department:", student[3])
            print("Email:", student[4])

        else:

            print("\nStudent not found. ❌")


    # ========================================
    # 4. SEARCH BY NAME
    # ========================================

    elif choice == "4":

        print("\n========== SEARCH BY NAME ==========")

        name = get_input(
            "Enter Student Name: "
        )

        students = search_by_name(name)

        display_students(students)


    # ========================================
    # 5. UPDATE STUDENT
    # ========================================

    elif choice == "5":

        print("\n========== UPDATE STUDENT ==========")

        roll_no = get_input(
            "Enter Roll Number: "
        )

        student = search_student(roll_no)

        if student:

            print("\nCurrent Details")

            print("Name:", student[1])
            print("Roll No:", student[2])
            print("Department:", student[3])
            print("Email:", student[4])

            print("\nEnter New Details")

            name = get_input(
                "Enter New Name: "
            )

            department = get_input(
                "Enter New Department: "
            )

            email = get_input(
                "Enter New Email: "
            )

            if not valid_email(email):

                print("\nInvalid email format.")

                continue

            result = update_student(
                roll_no,
                name,
                department,
                email
            )

            if result > 0:

                print(
                    "\nStudent updated successfully! ✅"
                )

            else:

                print(
                    "\nStudent update failed."
                )

        else:

            print("\nStudent not found. ❌")


    # ========================================
    # 6. DELETE STUDENT
    # ========================================

    elif choice == "6":

        print("\n========== DELETE STUDENT ==========")

        roll_no = get_input(
            "Enter Roll Number: "
        )

        student = search_student(roll_no)

        if student:

            print("\nStudent Details")

            print("Name:", student[1])
            print("Roll No:", student[2])
            print("Department:", student[3])
            print("Email:", student[4])

            confirm = input(
                "\nAre you sure you want to delete? (yes/no): "
            ).strip().lower()

            if confirm == "yes":

                result = delete_student(
                    roll_no
                )

                if result > 0:

                    print(
                        "\nStudent deleted successfully! ✅"
                    )

            else:

                print("\nDelete cancelled.")

        else:

            print("\nStudent not found. ❌")


    # ========================================
    # 7. STUDENT STATISTICS
    # ========================================

    elif choice == "7":

        print(
            "\n========== STUDENT STATISTICS =========="
        )

        total_students, department_counts = get_statistics()

        print(
            "\nTotal Students:",
            total_students
        )

        print(
            "\nDepartment-wise Students:"
        )

        if not department_counts:

            print("No students available.")

        else:

            for department, count in department_counts:

                print(
                    department,
                    ":",
                    count,
                    "student(s)"
                )


    # ========================================
    # 8. SEARCH BY DEPARTMENT
    # ========================================

    elif choice == "8":

        print(
            "\n========== SEARCH BY DEPARTMENT =========="
        )

        department = get_input(
            "Enter Department: "
        )

        students = search_by_department(
            department
        )

        display_students(students)


    # ========================================
    # 9. SORT STUDENTS
    # ========================================

    elif choice == "9":

        print(
            "\n========== SORT STUDENTS =========="
        )

        print("1. Sort by Name")
        print("2. Sort by Roll Number")
        print("3. Sort by Department")

        sort_option = input(
            "Enter your choice: "
        ).strip()

        students = sort_students(
            sort_option
        )

        if not students:

            print("\nInvalid sorting option.")

        else:

            print("\n========== SORTED STUDENTS ==========")

            display_students(students)


    # ========================================
    # 10. EXPORT TO CSV
    # ========================================

    elif choice == "10":

        print(
            "\n========== EXPORT STUDENTS =========="
        )

        result = export_students_to_csv()

        if result:

            print(
                "\nStudents exported successfully! ✅"
            )

            print(
                "File created: students.csv"
            )

        else:

            print(
                "\nNo students available to export. ❌"
            )


    # ========================================
    # 11. IMPORT FROM CSV
    # ========================================

    elif choice == "11":

        print(
            "\n========== IMPORT STUDENTS =========="
        )

        imported_count, skipped_count = (
            import_students_from_csv()
        )

        if imported_count == -1:

            print(
                "\nstudents.csv file not found. ❌"
            )

            print(
                "Please create students.csv first."
            )

        else:

            print(
                "\nCSV import completed! ✅"
            )

            print(
                "Students imported:",
                imported_count
            )

            print(
                "Students skipped:",
                skipped_count
            )


    # ========================================
    # 12. EXIT
    # ========================================

    elif choice == "12":

        print(
            "\n========================================"
        )

        print(
            "Thank you for using Student Management System!"
        )

        print(
            "Program exited successfully."
        )

        print(
            "========================================"
        )

        break


    # ========================================
    # INVALID CHOICE
    # ========================================

    else:

        print("\nInvalid choice!")

        print(
            "Please enter a number from 1 to 12."
        )