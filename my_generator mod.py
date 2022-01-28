nested_list = [
	['a', 'b', 'c'],
	['d', 'e', 'f'],
	[1, 2],
]

def flat_generator(some_list):
    for custom_list in some_list:
        if get_type(custom_list):
            yield custom_list
        else:
            yield from flat_generator(custom_list)

def get_type(var):
    if not isinstance(var, list):
	    return var

# for item in flat_generator(nested_list):
# 	print(item)

my_list = [item for item in flat_generator(nested_list)]
print(my_list)