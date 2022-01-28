nested_list = [
	['a', 'b', 'c'],
	['d', 'e', 'f', 'h', False],
	[1, 2, None],
]

class FlatIterator:
    def __init__(self, some_list):
      self.some_list = some_list
      self.cursor1 = 0
      self.cursor2 = -1

    def __iter__(self):
      return self

    def __next__(self):
      self.cursor2 += 1

      if len(self.some_list[self.cursor1]) > self.cursor2:

        return self.some_list[self.cursor1][self.cursor2]

      elif len(self.some_list[self.cursor1]) == self.cursor2:
        self.cursor1 += 1
        self.cursor2 = 0

        if self.cursor1 == len(self.some_list):
          raise StopIteration

        return self.some_list[self.cursor1][self.cursor2]

# for item in FlatIterator(nested_list):
# 	print(item)

flat_list = [item for item in FlatIterator(nested_list)]
print(flat_list)