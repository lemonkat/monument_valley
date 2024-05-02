def sum_lists(a, b):
	if type(a) is int:
		return a + b
	return [sum_lists(a[i], b[i]) for i in range(len(a))]

default = lambda x, d: d if x is None else x

def ndrange(inp):
	if len(inp) == 0:
		yield []
	else:
		for i in range(default(inp[0].start, 0), inp[0].stop, default(inp[0].step, 1)):
			for j in ndrange(inp[1:]):
				yield [i] + j

if __name__ == "__main__":
	for i in ndrange([slice(10), slice(2, 4, 1)]):
		print(i)
