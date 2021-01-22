import math
from typing import List, Set, Tuple
from constants import UTF_8


INPUT_FILE_NAME = "boarding_passes.txt"

N_ROWS = 128
N_COLS = 8
ROW_DIVISIONS = int(math.log2(N_ROWS))


def read_input_file() -> List[str]:
	all_lines = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			all_lines.append(line.strip())
	return all_lines


def seat_string_to_coord(seat_string: str) -> Tuple[int, int]:
	min_row = 0
	max_row = N_ROWS
	row_str = seat_string[:ROW_DIVISIONS]
	for c in row_str:
		half_mark = min_row + (max_row - min_row) // 2
		if c == "F":
			max_row = half_mark
		else:
			min_row = half_mark
	min_col = 0
	max_col = N_COLS
	col_str = seat_string[ROW_DIVISIONS:]
	for c in col_str:
		half_mark = min_col + (max_col - min_col) // 2
		if c == "L":
			max_col = half_mark
		else:
			min_col = half_mark
	return min_row, min_col


def seat_coord_to_int(row: int, col: int) -> int:
	return (row * N_COLS) + col


def get_all_seat_numbers(seat_strings: List[str]) -> Set[int]:
	seat_numbers = set()
	for seat_string in seat_strings:
		r, c = seat_string_to_coord(seat_string)
		seat_int = seat_coord_to_int(r, c)
		seat_numbers.add(seat_int)
	return seat_numbers


def find_missing_seat_number(seat_numbers: Set[int], max_number: int) -> int:
	for possible_number in range(1, max_number - 1):
		if possible_number in seat_numbers:
			continue
		if possible_number - 1 in seat_numbers and possible_number + 1 in seat_numbers:
			return possible_number
	return -1


if __name__ == "__main__":
	input_lines = read_input_file()
	seat_number_set = get_all_seat_numbers(input_lines)
	max_seat_number = max(seat_number_set)
	print("biggest seat number:", max_seat_number)
	missing_seat = find_missing_seat_number(seat_number_set, max_seat_number)
	print("your seat number:", missing_seat)
