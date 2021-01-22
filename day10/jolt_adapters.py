from typing import Dict, List, Set, Tuple
from constants import UTF_8


INPUT_FILE_NAME = "adapters.txt"


def read_input_file() -> List[int]:
	to_return = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line_ in in_file:
			line = line_.strip()
			to_return.append(int(line))
	return to_return


def make_graph(joltages: List[int]) -> Dict[int, Dict[int, int]]:
	n = len(joltages)
	graph = dict()
	for i in range(n):
		graph[i] = dict()
		in_joltage = joltages[i]
		for j in range(i + 1, n):
			out_joltage = joltages[j]
			diff = out_joltage - in_joltage
			if diff > 3:
				break
			graph[i][j] = diff
	return graph


def dfs_spanning_path(graph: Dict[int, Dict[int, int]], to_visit: int, target: int, path: List[int]) -> bool:
	if to_visit in path:
		return False
	path.append(to_visit)
	if to_visit == target:
		all_in = True
		for vertex in graph:
			if vertex not in path:
				all_in = False
				break
		if all_in:
			return True
	for neighbor in graph[path[-1]]:
		result = dfs_spanning_path(graph, neighbor, target, path)
		if result:
			return result
	path.pop(-1)
	return False


def path_to_costs(graph: Dict[int, Dict[int, int]], path: List[int]) -> List[int]:
	to_return = list()
	for i in range(len(path) - 1):
		to_return.append(graph[path[i]][path[i + 1]])
	return to_return


def count_1_and_3(costs: List[int]) -> Tuple[int, int]:
	ones = 0
	threes = 0
	for c in costs:
		if c == 1:
			ones += 1
		elif c == 3:
			threes += 1
	return ones, threes


def find_chunks(graph: Dict[int, Dict[int, int]], start_index: int, end_index: int) -> List[List[int]]:
	chunks = list()
	i = start_index
	while i < end_index:  # if i is at the last valid index then we need to stop
		furthest_neighbor = -1
		for neighbor in graph[i]:
			furthest_neighbor = max(neighbor, furthest_neighbor)
		if furthest_neighbor == -1:
			raise ValueError("NO NEIGHBORS FOUND!")
		new_furthest_neighbor = furthest_neighbor
		for j in range(i + 1, furthest_neighbor - 1):
			for neighbor in graph[j]:
				new_furthest_neighbor = max(neighbor, new_furthest_neighbor)
		chunks.append(list(range(i, new_furthest_neighbor + 1)))
		i = new_furthest_neighbor
	return chunks


def dfs_all_paths(graph: Dict[int, Dict[int, int]], to_visit: int, target: int, path: List[int], all_paths: Set[str]):
	if to_visit in path:
		return
	path.append(to_visit)
	if to_visit == target:
		all_paths.add(str(path))
		path.pop(-1)
		return
	for neighbor in graph[path[-1]]:
		dfs_all_paths(graph, neighbor, target, path, all_paths)
	path.pop(-1)


def count_paths_chunk(graph: Dict[int, Dict[int, int]], chunk: List[int]) -> int:
	all_paths = set()
	dfs_all_paths(graph, chunk[0], chunk[-1], [], all_paths)
	return len(all_paths)


def count_possible_paths(graph: Dict[int, Dict[int, int]], start_index: int, end_index: int) -> int:
	chunks = find_chunks(graph, start_index, end_index)
	product = 1
	for chunk in chunks:
		path_count = count_paths_chunk(graph, chunk)
		product *= path_count
	return product


if __name__ == "__main__":
	adapter_list = read_input_file()
	adapter_list.sort()
	num_adapters = len(adapter_list)
	device_joltage = 3 + adapter_list[-1]
	joltage_list = [0] + adapter_list + [device_joltage]
	source_index = 0
	device_index = num_adapters + 1
	g = make_graph(joltage_list)
	spanning_path = list()
	success = dfs_spanning_path(g, source_index, device_index, spanning_path)
	if not success:
		raise ValueError("NO ANSWER")
	spanning_path_costs = path_to_costs(g, spanning_path)
	count_1, count_3 = count_1_and_3(spanning_path_costs)
	print(f"product of {count_1} and {count_3}:", count_1 * count_3)
	arrangement_count = count_possible_paths(g, source_index, device_index)
	print("count of all possible arrangements:", arrangement_count)
