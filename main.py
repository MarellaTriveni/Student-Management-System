from database import add_student, view_students, search_student, update_student


print("================================")
print("   STUDENT MANAGEMENT SYSTEM")
print("================================")

print("1. Add Student")
print("2. View All Students")
print("3. Search Student")
print("4. Update Student")

choice = input("Enter your choice: ")


if choice == "1":

    name = input("Enter Student Name: ")
    roll_no = input("Enter Roll Number: ")
    department = input("Enter Department: ")
    email = input("Enter Email: ")

    add_student(name, roll_no, department, email)


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


elif choice == "4":

    roll_no = input("Enter Roll Number: ")

    student = search_student(roll_no)

    if student:

        print("\nCurrent Details:")
        print("Name:", student[1])
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
            print("Student updated successfully!")

    else:
        print("Student not found.")


else:
    print("Invalid choice!")