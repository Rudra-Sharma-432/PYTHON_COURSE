lis = map(int, input())
print(sum(lis))
# can be done useng while loop

n = int(input())
output = 0
while n > 0:
  output = output * 10 + n % 10
  n = n//10

print(output)