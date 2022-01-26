nested_list = [
	['a', 'b', 'c'],
	['d', 'e', 'f', 'h', False],
	[1, 2, None],
]

class FlatIterator:
    def __init__(self, some_list):
        self.some_list = some_list

    def __iter__(self):
      for custom_list in self.some_list:
        for i in custom_list:
            yield i

# for item in FlatIterator(nested_list):
# 	print(item)

flat_list = [item for item in FlatIterator(nested_list)]
print(flat_list)