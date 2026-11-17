list_a = [('a', 0), ('b', 2)]
print(type(list_a))

print('=' * 30)

dict_a = {
  'a': 0,
  'b': 2
}
dict_a_items = dict_a.items()

print(f"{dict_a_items = }")
print(f"{type(dict_a_items) = }")
print(f"{list(dict_a_items) = } ")


def eakFunction():
  print("hello people")



print("# 1. ==============")
list_b = [1,2,3]
list_b[2] = list_b.append(3)
print(list_b)


print("\n# 2. ==============")
x = 5
res = (x == 5) in [True] == True
print(res)


print("\n# 3. ==============")
def greet(name):
  print("hello", name)

greet
a = greet
a("from 'a'")
greet("from 'greet'")


print("\n# 4. ==============")
nums = [1, 2, 3]
gen = (x for x in nums if x in nums)
nums = [3, 4, 5]
print(list(gen))


print("\n# 5. ==============")
funcs = [lambda: i for i in range(3)]
i = 10
print([f() for f in funcs])


print("\n# 6. ==============")
d = {True: "yes", 1: "one", 1.0: "float"}
print(d)


print("\n# 7. ==============")
def tricky():
    x = [1]
    try:
        return x.append(2) or x
    finally:
        x = [99]
        return x

print(tricky())
