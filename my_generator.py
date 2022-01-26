nested_list = [
	['a', 'b', 'c'],
	['d', 'e', 'f'],
	[1, 2, None],
]

def flat_generator(some_list):
    for custom_list in some_list:
        for i in custom_list:
            yield i

# for item in flat_generator(nested_list):
# 	print(item)

my_list = [item for item in flat_generator(nested_list)]
print(my_list)