import re

from database import (
    add_student,
    view_students,
    search_student,
    update_student,
    delete_student,
    get_statistics
)


print("========================================")
print("      STUDENT MANAGEMENT SYSTEM")
print("========================================")


# Check empty input
def get_input(message):

    while True:

        value = input(message).strip()

        if value != "":
            return value

        print("Input cannot be empty. Please try again.")


# Check email
def valid_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern, email) is not None


# Check roll number
def valid_roll_number(roll_no):

    return roll_no.isdigit()


while True:

    print("\n========== MENU ==========")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Student Statistics")
    print("7. Exit")
    print("==========================")

    choice = input("Enter your choice: ").strip()


    # --------------------------------
    # 1. ADD STUDENT
    # --------------------------------

    if choice == "1":

        print("\n========== ADD STUDENT ==========")

        name = get_input("Enter Student Name: ")

        roll_no = get_input("Enter Roll Number: ")

        if not valid_roll_number(roll_no):

            print("\nRoll Number must contain only numbers.")
            continue

        department = get_input("Enter Department: ")

        email = get_input("Enter Email: ")

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


    # --------------------------------
    # 2. VIEW STUDENTS
    # --------------------------------

    elif choice == "2":

        print("\n========== ALL STUDENTS ==========")

        students = view_students()

        if not students:

            print("No students found.")

        else:

            for student in students:

                print("\nID:", student[0])
                print("Name:", student[1])
                print("Roll No:", student[2])
                print("Department:", student[3])
                print("Email:", student[4])

                print("----------------------------")


    # --------------------------------
    # 3. SEARCH STUDENT
    # --------------------------------

    elif choice == "3":

        print("\n========== SEARCH STUDENT ==========")

        roll_no = get_input("Enter Roll Number: ")

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


    # --------------------------------
    # 4. UPDATE STUDENT
    # --------------------------------

    elif choice == "4":

        print("\n========== UPDATE STUDENT ==========")

        roll_no = get_input("Enter Roll Number: ")

        student = search_student(roll_no)

        if student:

            print("\nCurrent Details")

            print("Name:", student[1])
            print("Roll No:", student[2])
            print("Department:", student[3])
            print("Email:", student[4])

            print("\nEnter New Details")

            name = get_input("Enter New Name: ")

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

                print("\nStudent updated successfully! ✅")

            else:

                print("\nStudent update failed.")

        else:

            print("\nStudent not found. ❌")


    # --------------------------------
    # 5. DELETE STUDENT
    # --------------------------------

    elif choice == "5":

        print("\n========== DELETE STUDENT ==========")

        roll_no = get_input("Enter Roll Number: ")

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

                result = delete_student(roll_no)

                if result > 0:

                    print("\nStudent deleted successfully! ✅")

            else:

                print("\nDelete cancelled.")


        else:

            print("\nStudent not found. ❌")


    # --------------------------------
    # 6. STATISTICS
    # --------------------------------

    elif choice == "6":

        print("\n========== STUDENT STATISTICS ==========")

        total_students, department_counts = get_statistics()

        print("\nTotal Students:", total_students)

        print("\nDepartment-wise Students:")

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


    # --------------------------------
    # 7. EXIT
    # --------------------------------

    elif choice == "7":

        print("\n========================================")
        print("Thank you for using Student Management System!")
        print("Program exited successfully.")
        print("========================================")

        break


    # --------------------------------
    # INVALID CHOICE
    # --------------------------------

    else:

        print("\nInvalid choice!")
        print("Please enter a number from 1 to 7.")