from typing import List, Set, Tuple
from constants import UTF_8


INPUT_FILE_NAME = "tiles.txt"

DIRECTIONS = {
	"e": (1, 0),
	"se": (1, -1),
	"sw": (0, -1),
	"w": (-1, 0),
	"nw": (-1, 1),
	"ne": (0, 1)
}


def read_input_file() -> List[str]:
	tiles = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			tiles.append(line.strip())
	return tiles


def parse_tile_directions(tile_directions: str) -> List[str]:
	n = len(tile_directions)
	i = 0
	j = 1
	parsed_directions = list()
	while i < n:
		if tile_directions[i:j] in DIRECTIONS:
			parsed_directions.append(tile_directions[i:j])
			i = j
		j += 1
	return parsed_directions


def get_black_tiles(tiles: List[List[str]]) -> Set[Tuple[int, int]]:
	# tiles start white
	black_tiles = set()
	for tile_directions in tiles:
		x = 0
		y = 0
		for direction in tile_directions:
			step_x, step_y = DIRECTIONS[direction]
			x += step_x
			y += step_y
		loc = (x, y)
		if loc in black_tiles:
			black_tiles.remove(loc)
		else:
			black_tiles.add(loc)
	return black_tiles


def count_black_neighbors(tile_loc: Tuple[int, int], black_tiles: Set[Tuple[int, int]]) -> int:
	x, y = tile_loc
	count = 0
	for step_x, step_y in DIRECTIONS.values():
		neighbor = (x + step_x, y + step_y)
		if neighbor in black_tiles:
			count += 1
	return count


def get_all_white_neighbors(black_tiles: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
	to_return = set()
	for x, y in black_tiles:
		for step_x, step_y in DIRECTIONS.values():
			neighbor = (x + step_x, y + step_y)
			if neighbor not in black_tiles:
				to_return.add(neighbor)
	return to_return


def execute_timestep(black_tiles: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
	to_remove = set()
	for tile_loc in black_tiles:
		black_neighbors = count_black_neighbors(tile_loc, black_tiles)
		if black_neighbors == 0 or black_neighbors > 2:
			to_remove.add(tile_loc)
	to_add = set()
	nearby_white_tiles = get_all_white_neighbors(black_tiles)
	for tile_loc in nearby_white_tiles:
		black_neighbors = count_black_neighbors(tile_loc, black_tiles)
		if black_neighbors == 2:
			to_add.add(tile_loc)
	if len(to_remove.intersection(to_add)) != 0:
		raise ValueError("there was a tile in both 'to_remove' and 'to_add'?")
	to_return = set()
	for tile_loc in black_tiles:
		if tile_loc not in to_remove:
			to_return.add(tile_loc)
	for tile_loc in to_add:
		to_return.add(tile_loc)
	return to_return


if __name__ == "__main__":
	tiles_raw = read_input_file()
	tiles_parsed = [parse_tile_directions(t) for t in tiles_raw]
	black_tiles_set = get_black_tiles(tiles_parsed)
	print(f"number of initial black tiles: {len(black_tiles_set)}")
	for _ in range(100):
		black_tiles_set = execute_timestep(black_tiles_set)
	print(f"number of black tiles after 100 steps: {len(black_tiles_set)}")
