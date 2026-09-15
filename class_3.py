print( 19 //  7) # 2
print( 19 // -7) # -3
print(-19 // -7) # 2
print(-19 //  7) # -3
print(-15 //  7) # -3


print("==========")
print(-19 % 7) # 2
print(19 % -7) # -2
print(-19 % -7) # -5
print(19 / -7, 19 % -7, 19 // -7) # -2.71428, -2, -3


# if deviser in the ' % ' is negative then the result will be negative
# the result of ' // ' will be floor value of the result of ' / '


print("==============")

print(7.5 / 2 ) # 3.75
print(7.5 // 2) # 3.0
print(7.5 % 2 ) # 1.5


# Priority of Operator:
## ()
## **
## +x, -x, ~x
## *, /, //, %
## +, -
## <<, >>
## &
## ^
## |
## <, <=, >, >=, ==, !=
## not x
## and
## or


print("================")
print(-2  ** 2 ) # -4
print((-2) ** 2) #  4
print(-2 ** -2 ) # -0.25

print(-2 ** -2 ** -2) # -0.8408964152537145
print(-(2 ** -(2 ** (-2)))) # -0.8408964152537145



import math

print("================")
print(len(str(2 ** 100)))
print(len(str(2 ** 105)))
print(len(str(2 ** 1000)))

import sys

print(sys.maxsize)