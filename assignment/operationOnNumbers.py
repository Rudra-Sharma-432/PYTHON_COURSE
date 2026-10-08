# lis = map(int, input())
# print(sum(lis))
# # can be done useng while loop
# 
# n = int(input())
# output = 0
# while n > 0:
#   output = output * 10 + n % 10
#   n = n//10
# 
# print(output)


num = input()
power = len(num)
num = int(num)
output = 0
while num > 0 :
  output +=  (num % 10) ** power
  num = num // 10
print(output)