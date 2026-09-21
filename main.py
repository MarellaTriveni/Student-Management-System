from database import add_student


print("================================")
print("   STUDENT MANAGEMENT SYSTEM")
print("================================")

name = input("Enter Student Name: ")
roll_no = input("Enter Roll Number: ")
department = input("Enter Department: ")
email = input("Enter Email: ")

add_student(name, roll_no, department, email)