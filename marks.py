print("Enter marks for 5 subjct out of 100")
sub1=float(input("Enter Subject1 marks:"))
sub2=float(input("Enter Subject2 marks:"))
sub3=float(input("Enter Subject3 marks:"))
sub4=float(input("Enter Subject4 marks:"))
sub5=float(input("Enter Subject5 marks:"))

total = sub1+sub2+sub3+sub4+sub5
percentege = (total/500)*100
print("***********Result***********")
print("Total marks:",total)
print("Percentage:",percentege)

if percentege>=75:
  print("Result:Distinction") #comment
elif percentege >=60:
  print("Result:First class")
elif percentege >=45:
  print("Result:pass")
else:
  print("Result:Fail")