a = 9

if a:
  print("yesss, a exist.")
else:
  print("this will not run") 


print(bool(0), bool(0.0), bool(""), bool(None)) # all Flase
print(bool(1), bool(5), bool("hi"), bool(-1)) # all True


print(0 or 5 or 9)  # 5
print("" or "hi")   # 'hi'
print(3 and 7)      # 7
print(0 and 7)      # 0

"""
or  : hunts for first truthy value
and : hunts for frist falsy value

default ; if nothings is found return the last value

"""


title = input("\nWrite your title (Mr/Ms/Mrs) : ") or 'Pro'
first_name = input("Write your first name : ") or 'Gen'
last_name = input("Write your last name : ") or 'Z'

print("\nHello,", title, first_name, last_name)
