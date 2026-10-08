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


# num = input()
# power = len(num)
# num = int(num)
# output = 0
# while num > 0 :
#   output +=  (num % 10) ** power
#   num = num // 10
# print(output)
 

# number = int(input())
# num = number
# correctness = 0
# length = 0
# 
# while number > 0:
#    length += 1
#    number = number//10
# 
# if length <= 9 :
#   number = num
# 
#   while number > 0:
#     if number % 10 <= (number %100 - number%10)//10:
#       print('not strictly incrsing')
#       break
#     else:
#       correctness +=1
#     number = number//10
# 
#   if correctness == length:
#     print("yes they are in incresing order")
# 
# else:
#   print("the number has more then 9 digits")

# num = int(input())
# output = 0
# i = 0
# while num > 0 :
#   if num % 10 != 0:
#     output = output + (num % 10)*(10**i)
#     i += 1
#     
#   num = num // 10
# 
# print(output)