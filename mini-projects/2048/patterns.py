n = int(input())
print()
i = 1
while i <= n:
  j = 1
  while j <= i:
    print(j, end=" ")
    j += 1
  i+= 1
  print()


print()

i = 1
while i <= n:
  j = 1
  print(" "*2*(n-i), end="")
  while j <= i:
    print(j, end=" ")
    j += 1
  i+= 1
  print()


print()

i = 1
while i <= n:
  j = i
  print(" "*2*(n-i), end="")
  while j >= 1:
    print(j, end=" ")
    j -= 1
  i+= 1
  print()

print()

i = 1
while i <= n:
  j = 1
  print(" "*2*(n-i), end="")
  while j <= i:
    print(j, end=" ")
    j += 1

  j-=2
  while j >= 1:
    print(j, end=" ")
    j -= 1

  i+= 1
  print()


print()

i = 0
while i < n:
  j = 0
  while j < n:
    if i == j  or i + j == n-1:
      print("*", end=" ")
    else:
      print(" ", end=" ")
    j += 1
  print()
  i += 1

print()

i = 0
while i < (2 * n) - 1:
  j = 0

  while j < (2 * n) - 1:
    if i + j >= n-1 and i - j >= -n+1 and i - j <= n-1 and i + j <= 3*n - 3:
      print("*", end=" ")
    else:
      print(" ", end=" ")

    j += 1
  i += 1
  print()