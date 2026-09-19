class Student:
    def __init__(self, name, roll_no, department, email):
        self.name = name
        self.roll_no = roll_no
        self.department = department
        self.email = email

    def display_details(self):
        print("----- Student Details -----")
        print("Name:", self.name)
        print("Roll No:", self.roll_no)
        print("Department:", self.department)
        print("Email:", self.email)
        print("---------------------------")


# Creating student objects

student1 = Student(
    "Triveni",
    "101",
    "CSE",
    "triveni@example.com"
)

student2 = Student(
    "Priya",
    "102",
    "CSE",
    "priya@example.com"
)
student3 = Student(
    "Rahul",
    "103",
    "ECE",
    "rahul@example.com"
)



# Display student details

student1.display_details()
student2.display_details()
student3.display_details()