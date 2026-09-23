print(int(bin(31), 2))
print(0b1101)
print(0x3d)

print("="*30)

print(bin(31))
print(oct(31))
print(hex(31))

print("="*30)

print(13 & 10)  # 8
# 13 => 1 1 0 1
# 10 => 1 0 1 0
# & =>  1 0 0 0 => 8

print(17 | 9)  # 25
# 17 => 1 0 0 0 1
#  9 => 0 1 0 0 1
#  | => 1 1 0 0 1 => 25

print(12 ^ 10)  # 6
# 12 => 1 1 0 0
# 10 => 1 0 1 0
#  ^ => 0 1 1 0  => 6

print(10 ^ 0)  # 10
# 10 => 1 0 1 0
#  0 => 0 0 0 0
#  ^ => 1 0 1 0  => 10


print("=" * 30)


print(10)
print(bin(10))
print(bin(10 << 2))
print(10 << 2) # 10 * (2^2)

print()

print(19)
print(bin(19))
print(bin(19 >> 3))
print(19 >> 3) # 19 * (2^(-3)) ~ 2

print()

# how to check if a number is odd
givenNum = int(input("Give a integer number to check if a numebr is odd or even: "))
if givenNum: 
  print("'givenNum & 1' gives:", givenNum & 1)
  if givenNum & 1 :
    print(givenNum, "is an odd number.")
  else:
    print(givenNum, "is an even number.")
else:
  print("You didnt typed any number.")

print("\n"+"=" * 30+"\n")

print(0.1 + 0.2)

print(0.5 + 0.25 == 0.75) # 1/2 + 1/4 = 3/4 (ez)
