year = (input("Type the year: "))

if year:
  year = int(year)
  if year % 400 == 0:
    print(year, "is a leap year")
  elif year % 100 == 0:
    print(year, "is not a leap year")
  elif year % 4 == 0:
    print(year, "is a leap year")
  else:
    print(year, "is not a leap year")

# year = int(input("Type the year: "))
# leapinfo = "a leap" if (year%400==0 or (year%4 == 0 and year%100 != 0)) else "not a leap"
# print(year, 'is', leapinfo, "year")



# 3n+1 problme
number = int(input("Type a number for '3n+1': "))
for i in range(1000):
  if number != 1:
    if number % 2 == 0:
      number = number//2
    else:
      number = 3 * number + 1

    print(number, " " * (4 - len(str(number))), "■" * number)

  else:
    break

# grading:
marks = int(input("Type your marks: "))
lst = ['A','B','C','D','E','F']
print(lst[max(9 - (marks-1)//10, 5)])


# voting
age = int(input("Type your age: "))
if age >= 18:
  print("You can vote.")


