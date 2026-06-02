students = ["Shravni","Shashank","Samiksha","Keshav","Snehal"]
Remaning_fess = ["1000","2000","4000","2000","4000"]
print("**********About Student Fess*****************")
def fess_structure(students,Remaning_fess):
   for student in range(5):
    if(4000>int(Remaning_fess[student]) ):
     print(f"Student Name={students[student]}=>fees is pending")
    else:
     print(f"Student Name={students[student]}=>fees is paid")
fess_structure(students,Remaning_fess)
    