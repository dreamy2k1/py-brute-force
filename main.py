from copy import deepcopy
import time


start = time.time()


def step_1(num):
	new = num * 64
	return (new ^ num) % 16777216


def step_2(num):
	new = num // 32
	return (new ^ num) % 16777216


def step_3(num):
	new = num * 2048
	return (new ^ num) % 16777216
	

def difference(seq):
	res = []
	for i in range(1, len(seq)):
		res.append(seq[i] - seq[i-1])
	return res


def get_indices(target, changes):
	res = []
	for change in changes:
		found = False
		for i in range(len(change) - 4):
			chunk = change[i:i+4]
			if chunk == target:
				res.append(i+4)
				found = True
				break
		if not found:
			res.append(None)
	return res


def get_profit(target, offers, changes):
	profit = 0
	for i, change in enumerate(changes):
		idx = get_index(target, change, 0)
		if idx != None:
			idx += 4
			profit += offers[i][idx]
	return profit


puzzle = 'sample_2.txt'
try:
	with open(puzzle) as fh:
		lines = fh.read().splitlines()
except:
	lines = '''
1
2
3
2024
'''
	lines = lines.splitlines()[1:]

repeat = 2000
offers = []
changes = []
for line in lines:
	num = int(line)
	paying = [num % 10]
	for i in range(repeat):
		num = step_1(num)
		num = step_2(num)
		num = step_3(num)
		paying.append(num % 10)

	offers.append(deepcopy(paying))	 # records the price sequence for each monkey
	changes.append(difference(paying))  # records the price changes for each monkey
	

visited = []
highest = 0
quest = None	# instructed sequence
for z, change in enumerate(changes):
	print(f'Monkey at index {z}.')

	# for each changes sequence, grab four prices changes
	# use that to find how much we can get for all monkeys
	# if the changes sequence as seen before, skip it, otherwise, add to visited
	for c in range(len(change) - 4):
		target = change[c:c+4]
		if target in visited:
			continue
		else:
			visited.append(target)
			
		indices = get_indices(target, changes)

		tmp = 0
		for j, idx in enumerate(indices):
			if idx != None:
				tmp += offers[j][idx]
		if tmp > highest:
			highest = tmp
			quest = target

print(f'Ans: {highest}, instructed sequence: {quest}')


end = time.time()
print(f'Time spent with {len(lines)} monkeys in queening: {end - start} seconds.')
