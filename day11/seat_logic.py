import numpy as np
from constants import UTF_8


INPUT_FILE_NAME = "seats.txt"

FLOOR = -1
SEAT_EMPTY = 0
SEAT_OCCUPIED = 1


def read_input_file() -> np.ndarray:
	all_rows = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			row = list()
			for c in line.strip():
				if c == "L":
					row.append(SEAT_EMPTY)
				elif c == ".":
					row.append(FLOOR)
				elif c == "#":
					row.append(SEAT_OCCUPIED)
				else:
					raise ValueError(f"UNKNOWN INPUT VALUE: {c}")
			all_rows.append(np.array(row))
	return np.stack(all_rows)


def count_occupied_visible_seats(seats: np.ndarray, target_row: int, target_col: int) -> int:
	count = 0
	for row_shift in [-1, 0, 1]:
		for col_shift in [-1, 0, 1]:
			if row_shift == 0 and col_shift == 0:
				continue  # don't count the center
			row = target_row + row_shift
			col = target_col + col_shift
			while 0 <= row < seats.shape[0] and 0 <= col < seats.shape[1]:
				# stay in bounds
				# if we see a seat, that's the end of our line of sight
				if seats[row, col] == SEAT_EMPTY:
					break
				elif seats[row, col] == SEAT_OCCUPIED:
					count += 1
					break
				else:  # not a seat; keep looking in this direction
					row += row_shift
					col += col_shift
	return count


def advance_time(seats: np.ndarray) -> np.ndarray:
	new_seats = np.empty_like(seats)
	for i in range(seats.shape[0]):
		for j in range(seats.shape[1]):
			if seats[i, j] == FLOOR:
				new_seats[i, j] = FLOOR
				continue
			occupied_neighbors_count = count_occupied_visible_seats(seats, i, j)
			if seats[i, j] == SEAT_EMPTY and occupied_neighbors_count == 0:
				new_seats[i, j] = SEAT_OCCUPIED
			elif seats[i, j] == SEAT_OCCUPIED and occupied_neighbors_count >= 5:
				new_seats[i, j] = SEAT_EMPTY
			else:
				new_seats[i, j] = seats[i, j]
	return new_seats


if __name__ == "__main__":
	seat_array = read_input_file()
	time_step_count = 0
	repeat = True
	while repeat:
		new_seat_array = advance_time(seat_array)
		time_step_count += 1
		repeat = (not np.array_equal(seat_array, new_seat_array))
		seat_array = new_seat_array
	occupied_count = np.count_nonzero(seat_array == SEAT_OCCUPIED)
	print(f"{time_step_count} time steps passed")
	print("number of occupied seats after things settle down:", occupied_count)
