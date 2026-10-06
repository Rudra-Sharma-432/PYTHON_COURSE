times = int(input("type an int: "))
for i in range(times):
  print(i)


while True:
  cmd = input("Type Command: ")
  if cmd == 'quit':
    print("bye!")
    break
  print('You said:', cmd)


tryleft = 5
while True:
  if tryleft == 0:
    print("No try left")
    break
  
  keypass = int(input("Type the pin: "))
  
  if keypass == 123456:
    print("vault unlocked")
    break
  print('Wrong pin:', keypass , '\nTry again. You have', tryleft, "try left.")

  tryleft -= 1