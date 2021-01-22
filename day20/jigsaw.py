import time
import numpy as np
import re
from typing import Dict, List, Set, Tuple
from constants import UTF_8


INPUT_FILE_NAME = "tiles.txt"

TILE_SIZE = 10
TILE_HEADER_RE = re.compile(r"Tile ([0-9]+):")
R = "R"
D = "D"
L = "L"
U = "U"
EDGES = [R, D, L, U]  # the order of this is important


MONSTER_FILE_NAME = "monster.txt"


def get_monster_mask() -> np.ndarray:
	lines = list()
	with open(MONSTER_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			lines.append(line[:-1])
	longest = max((len(line) for line in lines))
	rows = list()
	for line_ in lines:
		line = line_ + "".join([" "] * (longest - len(line_)))  # the spaces at the end of lines keep disappearing. I think this IDE is removing them
		row = np.array([c == "#" for c in line])
		rows.append(row)
	return np.stack(rows)


def get_mask_as_tuples(mask: np.ndarray) -> List[Tuple[int, int]]:
	tuples = list()
	for i in range(mask.shape[0]):
		for j in range(mask.shape[1]):
			if mask[i, j]:
				tuples.append((i, j))
	return tuples


MONSTER_MASK = get_monster_mask()
MONSTER_TUPLES = get_mask_as_tuples(MONSTER_MASK)


def read_input_file() -> Dict[int, np.ndarray]:
	tiles = dict()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		while True:
			header_line = in_file.readline()
			if header_line == "":
				break
			match = TILE_HEADER_RE.fullmatch(header_line.strip())
			tile_id = int(match.group(1))
			rows = list()
			for _ in range(TILE_SIZE):
				line = in_file.readline().strip()
				rows.append(np.array([c == "#" for c in line]))
			tile = np.stack(rows)
			tiles[tile_id] = tile
			in_file.readline()  # eat the empty line
	return tiles


def get_edge(edge: str, flip: bool, tile: np.ndarray) -> np.ndarray:
	if edge == R:
		to_return = tile[:, -1]
		actual_flip = flip
	elif edge == U:
		to_return = tile[0, :]
		actual_flip = flip
	elif edge == L:
		to_return = tile[:, 0]
		actual_flip = not flip
	elif edge == D:
		to_return = tile[-1, :]
		actual_flip = not flip
	else:
		raise ValueError("Unknown edge direction!")
	if actual_flip:
		return to_return[::-1]
	else:
		return to_return


def create_adjacency_list(ids: List[int], tiles: Dict[int, np.ndarray]) -> Dict[int, Dict[str, Set[Tuple[int, str]]]]:
	n = len(ids)
	adjacency = dict()
	for i in range(n):  # make empty dict for every vertex/piece/tile
		adjacency[i] = dict()
		for e in EDGES:
			adjacency[i][e] = set()
	# find pieces that could be adjacent
	for i in range(n):
		tile_i = tiles[ids[i]]
		for e_i in EDGES:
			edge_i = get_edge(e_i, False, tile_i)
			for j in range(i + 1, n):  # this is symmetric, so we can do an upper triangular deal
				tile_j = tiles[ids[j]]
				for e_j in EDGES:
					for flip_j in [False, True]:
						edge_j = get_edge(e_j, flip_j, tile_j)
						if np.array_equal(edge_i, edge_j):  # the edges match
							adjacency[i][e_i].add((j, e_j))
							adjacency[j][e_j].add((i, e_i))
	return adjacency


def find_corners(adjacency: Dict[int, Dict[str, Set[Tuple[int, str]]]]) -> List[int]:
	corner_tiles = list()
	edge_count = 0
	center_count = 0
	for index, inner_dict in adjacency.items():
		count = 0
		for neighbors in inner_dict.values():
			count += len(neighbors)
		if count == 2:
			corner_tiles.append(index)
		elif count == 3:
			edge_count += 1
		elif count == 4:
			center_count += 1
		else:
			raise ValueError("found a piece with a number of matching neighbors that was not 2, 3, or 4")
	if len(corner_tiles) != 4:
		raise ValueError("Didn't find exactly 4 corners")
	if edge_count != 40:
		raise ValueError("Didn't find exactly 40 edges")
	if center_count != 100:
		raise ValueError("Didn't find exactly 100 centers")
	return corner_tiles


def print_answer_part_1(corner_tiles: List[int], ids: List[int]):
	corner_ids = [ids[index] for index in corner_tiles]
	product = 1
	for id_num in corner_ids:
		product *= id_num
	print(f"product of all 4 corner IDs: {product}")


def find_good_sides(tile: int, adjacency: Dict[int, Dict[str, Set[Tuple[int, str]]]]) -> List[str]:
	good_sides = list()
	for edge, neighbors in adjacency[tile].items():
		if len(neighbors) == 1:
			good_sides.append(edge)
		elif len(neighbors) > 1:
			raise ValueError("multiple neighbors in the same direction?")
	return good_sides


def build_first_row(first: int, adjacency: Dict[int, Dict[str, Set[Tuple[int, str]]]]) -> List[Tuple[int, int, bool]]:
	first_row = list()
	# upper-left corner
	good_sides = find_good_sides(first, adjacency)
	if R in good_sides and D in good_sides:
		r = 0
	elif D in good_sides and L in good_sides:
		r = 1
	elif L in good_sides and U in good_sides:
		r = 2
	elif U in good_sides and R in good_sides:
		r = 3
	else:
		raise ValueError("bad edge combo for the first corner")
	first_row.append((first, r, False))
	# do all the top 10 edge pieces
	for _ in range(10):
		previous, previous_r, previous_flip = first_row[-1]
		if previous_flip:
			previous_r = (previous_r + 2) % 4
		neighbors = adjacency[previous][EDGES[previous_r]]
		if len(neighbors) != 1:
			raise ValueError("not the right number of neighbors!")
		current, current_e = list(neighbors)[0]
		good_sides = find_good_sides(current, adjacency)
		if U not in good_sides:
			r = 0
			flip = (current_e == R)
		elif R not in good_sides:
			r = 1
			flip = (current_e == D)
		elif D not in good_sides:
			r = 2
			flip = (current_e == L)
		elif L not in good_sides:
			r = 3
			flip = (current_e == U)
		else:
			raise ValueError("This was supposed to be an edge (only 3 good sides)")
		first_row.append((current, r, flip))
	# do the upper-right corner
	previous, previous_r, previous_flip = first_row[-1]
	if previous_flip:
		previous_r = (previous_r + 2) % 4
	neighbors = adjacency[previous][EDGES[previous_r]]
	if len(neighbors) != 1:
		raise ValueError("not the right number of neighbors!")
	current, current_e = list(neighbors)[0]
	good_sides = find_good_sides(current, adjacency)
	if R in good_sides and D in good_sides:
		if current_e == D:
			r = 3
			flip = False
		else:
			r = 0
			flip = True
	elif D in good_sides and L in good_sides:
		if current_e == L:
			r = 0
			flip = False
		else:
			r = 1
			flip = True
	elif L in good_sides and U in good_sides:
		if current_e == U:
			r = 1
			flip = False
		else:
			r = 2
			flip = True
	elif U in good_sides and R in good_sides:
		if current_e == R:
			r = 2
			flip = False
		else:
			r = 3
			flip = True
	else:
		raise ValueError("bad edge combo for the first corner")
	first_row.append((current, r, flip))
	return first_row


def build_next_row(previous_row: List[Tuple[int, int, bool]], adjacency: Dict[int, Dict[str, Set[Tuple[int, str]]]]) -> List[Tuple[int, int, bool]]:
	n = len(previous_row)
	row = list()
	# left-most piece
	above, above_r, _ = previous_row[0]
	neighbors = adjacency[above][EDGES[(above_r + 1) % 4]]
	if len(neighbors) != 1:
		raise ValueError("not the right number of neighbors!")
	current, current_e = list(neighbors)[0]
	r = (EDGES.index(current_e) + 1) % 4
	good_sides = find_good_sides(current, adjacency)
	flip = (EDGES[(2 + r) % 4] in good_sides)
	row.append((current, r, flip))
	# rest of the row
	for i in range(1, n):
		previous, previous_r, previous_flip = row[-1]
		if previous_flip:
			previous_r = (previous_r + 2) % 4
		neighbors_left = adjacency[previous][EDGES[previous_r]]
		if len(neighbors_left) != 1:
			raise ValueError("not the right number of neighbors!")
		current, current_e_left = list(neighbors_left)[0]
		above, above_r, _ = previous_row[i]
		neighbors_above = adjacency[above][EDGES[(above_r + 1) % 4]]
		if len(neighbors_above) != 1:
			raise ValueError("not the right number of neighbors!")
		current_, current_e_above = list(neighbors_above)[0]
		if current != current_:
			raise ValueError("the pieces from left and above don't agree on which tile should go next")
		r = (EDGES.index(current_e_above) + 1) % 4
		r_index_to_go_left = (r - EDGES.index(current_e_left)) % 4
		if r_index_to_go_left == 0:
			flip = True
		elif r_index_to_go_left == 2:
			flip = False
		else:
			raise ValueError("things don't line up with matching the top tile and the left tile")
		row.append((current, r, flip))
	return row


def solve_puzzle(first: int, adjacency: Dict[int, Dict[str, Set[Tuple[int, str]]]]) -> List[List[Tuple[int, int, bool]]]:
	rows = list()
	rows.append(build_first_row(first, adjacency))
	for _ in range(11):  # we know there are exactly 12 rows
		rows.append(build_next_row(rows[-1], adjacency))
	return rows


def reconstruct_image(instructions: List[List[Tuple[int, int, bool]]], ids: List[int], tiles: Dict[int, np.ndarray]) -> np.ndarray:
	rows = list()
	for row_instruction in instructions:
		row = list()
		for index, r, flip in row_instruction:
			trimmed_tile = tiles[ids[index]][1:-1, 1:-1]
			rotated_tile = np.rot90(trimmed_tile, r)
			if flip:
				row.append(rotated_tile[:, ::-1])
			else:
				row.append(rotated_tile)
		rows.append(np.concatenate(row, axis=1))
	return np.concatenate(rows, axis=0)


def find_monsters(image: np.ndarray) -> List[Tuple[int, int]]:
	monster_locations = list()
	for i in range(image.shape[0] + 1 - MONSTER_MASK.shape[0]):
		for j in range(image.shape[1] + 1 - MONSTER_MASK.shape[1]):
			found_monster = True
			for i_shift, j_shift in MONSTER_TUPLES:
				if not image[i + i_shift, j + j_shift]:
					found_monster = False
					break
			if found_monster:
				monster_locations.append((i, j))
	return monster_locations


def count_marks_no_monsters(image: np.ndarray, monster_locations: List[Tuple[int, int]]) -> int:
	edited_image = np.copy(image)
	for i, j in monster_locations:
		for i_shift, j_shift in MONSTER_TUPLES:
			edited_image[i + i_shift, j + j_shift] = False
	return np.count_nonzero(edited_image)


if __name__ == "__main__":
	time_start = time.time()
	tiles_dict = read_input_file()
	tile_id_list = list(tiles_dict.keys())
	adjacency_list = create_adjacency_list(tile_id_list, tiles_dict)
	corner_indices = find_corners(adjacency_list)
	print_answer_part_1(corner_indices, tile_id_list)
	construction_instructions = solve_puzzle(corner_indices[0], adjacency_list)
	full_image = reconstruct_image(construction_instructions, tile_id_list, tiles_dict)
	images_to_try = list()
	for rotation in range(4):
		full_image_rotated = np.rot90(full_image, rotation)
		for flip_image in [False, True]:
			if flip_image:
				images_to_try.append(full_image_rotated[:, ::-1])
			else:
				images_to_try.append(full_image_rotated)
	found_monsters = False
	for img in images_to_try:
		locations = find_monsters(img)
		if len(locations) != 0:  # found some!
			if found_monsters:
				print("we found multiple images with monsters!")
			found_monsters = True
			marks_counted = count_marks_no_monsters(img, locations)
			print(f"marks found, ignoring monsters: {marks_counted}")
			time_end = time.time()
			print(f"time elapsed: {time_end - time_start} sec")
