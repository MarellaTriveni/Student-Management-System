from database import (
    add_student,
    view_students,
    search_student,
    update_student,
    delete_student
)


print("================================")
print("   STUDENT MANAGEMENT SYSTEM")
print("================================")

print("1. Add Student")
print("2. View All Students")
print("3. Search Student")
print("4. Update Student")
print("5. Delete Student")

choice = input("Enter your choice: ")


# 1. Add Student
if choice == "1":

    name = input("Enter Student Name: ")
    roll_no = input("Enter Roll Number: ")
    department = input("Enter Department: ")
    email = input("Enter Email: ")

    add_student(name, roll_no, department, email)


# 2. View All Students
elif choice == "2":

    students = view_students()

    print("\n========== ALL STUDENTS ==========")

    if len(students) == 0:
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

    roll_no = input("Enter Roll Number: ")

    student = search_student(roll_no)

    if student:

        print("\n========== STUDENT FOUND ==========")
        print("ID:", student[0])
        print("Name:", student[1])
        print("Roll No:", student[2])
        print("Department:", student[3])
        print("Email:", student[4])

    else:
        print("Student not found.")


# 4. Update Student
elif choice == "4":

    roll_no = input("Enter Roll Number: ")

    student = search_student(roll_no)

    if student:

        print("\n========== CURRENT DETAILS ==========")
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
        print("Student not found.")


# 5. Delete Student
elif choice == "5":

    roll_no = input("Enter Roll Number: ")

    student = search_student(roll_no)

    if student:

        print("\n========== STUDENT DETAILS ==========")
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
            print("\nDelete operation cancelled.")

    else:
        print("Student not found.")


# Invalid choice
else:
    print("Invalid choice!")