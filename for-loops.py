print(type(range(5))) # range
print(range(5)) # 'range(0, 5)'
print(list(range(5))) # [0, 1, 2, 3, 4]

# in range(a, b, n) the second number is not reached
# [9, 7, 5, 3]
print(list(range(9, 1, -2))) 

# writing a 'for loop'
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

print('=' * 30)

fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")

print('=' * 30)

# this loop can only work on 'list', 'tuple'
# and will give error on 'set'
items = ['hi', 0, 10, 5]
i = 0
while i < len(items):
    print(items[i])
    i += 1

print('=' * 30)

# writing the same 'for loop' in terms of 'while loop'
fruits = ["apple", "banana", "cherry"]
## Step 1: Create an iterator object from the iterable
iterator = iter(fruits)
print(iterator)
## Step 2: Run an infinite while loop
while True:
    try:
        ## Step 3: Fetch the next item
        fruit = next(iterator)
        print(fruit)
    except StopIteration:
        ## Step 4: Exit the loop when items run out
        print('iteration done by while loop')
        break



print('=' * 30)


set_a = {20,4,5,3,2,5,6,7,8,46,3,6,10,5,6,8,9,}
for element in set_a:
    print(element)


# after all that we got some left off variables 
print('=' * 30)
print(f"{element = }")
print(f"{fruit = }")
print(f"{i = }")


print('=' * 30)

def print_table(n):
    for _ in range(1, 11):
        print(f"{n} x {_} = {n * _}")
    print()
print_table(9)

print('=' * 30)

r  = 5
for i in range(5):
    print(i)
    i = i - 1



def make_dict(dict_input):
    splited = (dict_input.split(' / '))
    splited.pop(0)
    output = {}
    for val in splited:
        key = val.split()[0]
        value = val.split()[1]
        output[key] = int(value)
    return output

marks_dict = make_dict(input())
print(marks_dict)