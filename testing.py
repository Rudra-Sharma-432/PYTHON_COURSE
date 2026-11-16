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
