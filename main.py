from database import (
    add_student,
    view_students,
    search_student,
    update_student,
    delete_student
)


def get_required_input(message):
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Input cannot be empty. Please try again.")


print("================================")
print("   STUDENT MANAGEMENT SYSTEM")
print("================================")


while True:

    print("\n========== MENU ==========")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice: ").strip()


    # 1. Add Student
    if choice == "1":

        print("\n========== ADD STUDENT ==========")

        name = get_required_input("Enter Student Name: ")
        roll_no = get_required_input("Enter Roll Number: ")
        department = get_required_input("Enter Department: ")
        email = get_required_input("Enter Email: ")

        add_student(
            name,
            roll_no,
            department,
            email
        )


    # 2. View Students
    elif choice == "2":

        print("\n========== ALL STUDENTS ==========")

        students = view_students()

        if not students:
            print("No students found.")

        else:
            for student in students:

                print("ID:", student[0])
                print("Name:", student[1])
                print("Roll No:", student[2])
                print("Department:", student[3])
                print("Email:", student[4])
                print("--------------------------------")


    # 3. Search Student
    elif choice == "3":

        print("\n========== SEARCH STUDENT ==========")

        roll_no = get_required_input("Enter Roll Number: ")

        student = search_student(roll_no)

        if student:

            print("\nStudent Found!")
            print("ID:", student[0])
            print("Name:", student[1])
            print("Roll No:", student[2])
            print("Department:", student[3])
            print("Email:", student[4])

        else:

            print("Student not found.")


    # 4. Update Student
    elif choice == "4":

        print("\n========== UPDATE STUDENT ==========")

        roll_no = get_required_input("Enter Roll Number: ")

        student = search_student(roll_no)

        if student:

            print("\nCurrent Details:")
            print("Name:", student[1])
            print("Roll No:", student[2])
            print("Department:", student[3])
            print("Email:", student[4])

            print("\nEnter New Details")

            name = get_required_input("Enter New Name: ")
            department = get_required_input("Enter New Department: ")
            email = get_required_input("Enter New Email: ")

            result = update_student(
                roll_no,
                name,
                department,
                email
            )

            if result > 0:
                print("\nStudent updated successfully!")

        else:

            print("Student not found.")


    # 5. Delete Student
    elif choice == "5":

        print("\n========== DELETE STUDENT ==========")

        roll_no = get_required_input("Enter Roll Number: ")

        student = search_student(roll_no)

        if student:

            print("\nStudent Details:")
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
                    print("\nStudent deleted successfully!")

            else:

                print("\nDelete operation cancelled.")

        else:

            print("Student not found.")


    # 6. Exit
    elif choice == "6":

        print("\nThank you for using Student Management System!")
        print("Program exited successfully.")

        break


    # Invalid choice
    else:

        print("\nInvalid choice!")
        print("Please enter a number from 1 to 6.")