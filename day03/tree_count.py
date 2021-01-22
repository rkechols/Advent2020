import numpy as np
from constants import UTF_8


INPUT_FILE_NAME = "trees.txt"


def read_input_file() -> np.ndarray:
	all_rows = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line_ in in_file:
			line = line_.strip()
			row = np.array([c == "#" for c in line])
			all_rows.append(row)
	return np.stack(all_rows)


def count_collision(trees: np.ndarray, col_shift: int, row_shift: int) -> int:
	count = 0
	row = 0
	col = 0
	while row < trees.shape[0]:
		if trees[row, col]:
			count += 1
		row += row_shift
		col += col_shift
		col %= trees.shape[1]
	return count


if __name__ == "__main__":
	tree_array = read_input_file()
	tree_count = count_collision(tree_array, 3, 1)
	print("collisions for (3, 1):", tree_count)
	other_slopes = [(1, 1), (5, 1), (7, 1), (1, 2)]
	for c_shift, r_shift in other_slopes:
		tree_count *= count_collision(tree_array, c_shift, r_shift)
	print("product of all collisions:", tree_count)
