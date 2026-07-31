coaching_info = {
    "name": "Apex Academy",
    "city": "Pune",
    "course": "python",
    "Teacher": "Parhad Sir",
    "Total Students": 120,
    "Timings": "10am to 5pm"
}


students = [
    {"id": 1, "name": "Rahul", "course": "python", "fees": 5000, "status": "Active"},
    {"id": 2, "name": "Sham", "course": "java", "fees": 4000, "status": "Active"},
    {"id": 3, "name": "Shashank", "course": "python", "fees": 5000, "status": "Inactive"},
    {"id": 4, "name": "Samarth", "course": "C++", "fees": 3500, "status": "Active"},
    {"id": 5, "name": "Keshav", "course": "C language", "fees": 3000, "status": "Active"}
]

def get_status(student):
    return student["status"]

print("Students Data:")
for student in students:
    print(student)
    print("Status:", get_status(student))
    print("----------------------------------")

teacher_info = {
    "Teacher_name": "Parhad Sir",
    "Subject": "python",
    "Experience": "10 years"
}


def search_records(name):
    for student in students:
        if student["name"].lower() == name.lower():
            return student
    return "student not found"
print("*****************************************************")
# Search example
print(search_records("Rahul"))