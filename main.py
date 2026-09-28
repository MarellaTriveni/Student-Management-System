from database import (
    add_student,
    view_students,
    search_student,
    update_student,
    delete_student,
    get_statistics
)


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
    print("6. Student Statistics")
    print("7. Exit")
    print("==========================")

    choice = input("Enter your choice: ")


    # 1. ADD STUDENT
    if choice == "1":

        print("\n========== ADD STUDENT ==========")

        name = input("Enter Student Name: ")
        roll_no = input("Enter Roll Number: ")
        department = input("Enter Department: ")
        email = input("Enter Email: ")

        add_student(
            name,
            roll_no,
            department,
            email
        )


    # 2. VIEW ALL STUDENTS
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


    # 3. SEARCH STUDENT
    elif choice == "3":

        print("\n========== SEARCH STUDENT ==========")

        roll_no = input("Enter Roll Number: ")

        student = search_student(roll_no)

        if student:

            print("\nStudent Found!")
            print("ID:", student[0])
            print("Name:", student[1])
            print("Roll No:", student[2])
            print("Department:", student[3])
            print("Email:", student[4])

        else:

            print("\nStudent not found.")


    # 4. UPDATE STUDENT
    elif choice == "4":

        print("\n========== UPDATE STUDENT ==========")

        roll_no = input("Enter Roll Number: ")

        student = search_student(roll_no)

        if student:

            print("\nCurrent Details")
            print("Name:", student[1])
            print("Roll No:", student[2])
            print("Department:", student[3])
            print("Email:", student[4])

            print("\nEnter New Details")

            name = input("Enter New Name: ")
            department = input("Enter New Department: ")
            email = input("Enter New Email: ")

            result = update_student(
                roll_no,
                name,
                department,
                email
            )

            if result > 0:
                print("\nStudent updated successfully!")

        else:

            print("\nStudent not found.")


    # 5. DELETE STUDENT
    elif choice == "5":

        print("\n========== DELETE STUDENT ==========")

        roll_no = input("Enter Roll Number: ")

        student = search_student(roll_no)

        if student:

            print("\nStudent Details")
            print("Name:", student[1])
            print("Roll No:", student[2])
            print("Department:", student[3])
            print("Email:", student[4])

            confirm = input(
                "\nAre you sure you want to delete? (yes/no): "
            )

            if confirm.lower() == "yes":

                result = delete_student(roll_no)

                if result > 0:
                    print("\nStudent deleted successfully!")

            else:

                print("\nDelete cancelled.")

        else:

            print("\nStudent not found.")


    # 6. STUDENT STATISTICS
    elif choice == "6":

        print("\n========== STUDENT STATISTICS ==========")

        total_students, department_counts = get_statistics()

        print("\nTotal Students:", total_students)

        print("\nDepartment-wise Students:")

        if not department_counts:

            print("No students available.")

        else:

            for department, count in department_counts:

                print(department, ":", count)


    # 7. EXIT
    elif choice == "7":

        print("\nThank you for using Student Management System!")
        print("Program exited successfully.")

        break


    # INVALID CHOICE
    else:

        print("\nInvalid choice. Please enter 1 to 7.")