# def getMetrix():
#   r, c = map(int, input("give rows and column in `<r> <c>` format:\n").split())
#   A = []
#   for i in range(r):
#     L = list(map(int, input(f"Give {i+1}-th row\n").split()))
#     if len(L) == c:
#       A.append(L)
#     else:
#       print('You printed wrong amount of elements.')
#       return []
#   print()
#   return(A)
# 
# def printMatrix(M):
#   i = 0
#   while i < len(M):
#     j = 0
#     while j < len(M[0]):
#       print(M[i][j], end=" ")
#       j += 1
#     print()
#     i += 1
# 
# def rotate90(A):
#   rows = len(A)
#   cols = len(A[0])
#   B = []
#   j = 0
#   while j < cols:
#     lst = []
#     i = rows - 1
#     while i >= 0:
#       lst.append(A[i][j])
#       i -= 1
#     B.append(lst)  
#     j += 1
# 
#   return(B)
# 
# 
# 
# 
# def rotate180(M):
#   B = []
#   i = len(M) - 1
#   while i >= 0:
#     lst = []
#     j = len(M[0]) - 1
#     while j >= 0:
#       lst.append(M[i][j])
#       j -= 1
#     B.append(lst)
#     i -= 1
# 
#   return(B)
# 
# 
# 
# A = getMetrix()
# 
# print("given matrix")
# printMatrix(A)
# 
# print("\nmatrix after rotating by 90 deg")
# printMatrix(rotate90(A))
# 
# print("\nmatrix after rotating by 180 deg")
# printMatrix(rotate180(A))
# 


# ==============================================
print("="*20)

def giveAntiDiagnol(M):
  i = 0
  j = 0

  down = False
  
  while not(i == (len(M) - 1) and j == (len(M[0]) - 1)):

    print(i, j)
    print(down)
    print(M[i][j])
    print()

    i += 1
    j -= 1

    if (j < 0) or i >= len(M):
      if down:
        i = (i + j + 1) - len(M[0]) - 1
      else:
        i, j = i - i, j + i

      if down:
        j = len(M[0]) - 1
      else:
        j = (i + j + 1)


      if j == len(M[0]) - 1:
        down = True


  # print(i != (len(M) - 1) and j != (len(M[0]) - 1) , i , j, len(M), len(M[0]))


A = [
  [1, 2, 3, 0],
  [4, 5, 6, 1],
  [7, 8, 9, 2]
]
giveAntiDiagnol(A)