import numpy as np
from constants import UTF_8


INPUT_FILE_NAME = "cubes_initial.txt"
SHIFTS = [-1, 0, 1]


def read_input_file() -> np.ndarray:
	rows = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			row = list()
			for c in line.strip():
				row.append(c == "#")
			rows.append(np.array(row))
	to_return = np.stack(rows, axis=0)
	to_return = np.stack([to_return], axis=2)
	to_return = np.stack([to_return], axis=3)
	return to_return


def add_row(a: np.ndarray, row_goes_above: bool) -> np.ndarray:
	new_row = np.stack([np.zeros_like(a[0, :, :, :])], axis=0)
	if row_goes_above:
		return np.concatenate([new_row, a], axis=0)
	else:
		return np.concatenate([a, new_row], axis=0)


def add_col(a: np.ndarray, col_goes_left: bool) -> np.ndarray:
	new_col = np.stack([np.zeros_like(a[:, 0, :, :])], axis=1)
	if col_goes_left:
		return np.concatenate([new_col, a], axis=1)
	else:
		return np.concatenate([a, new_col], axis=1)


def add_layer(a: np.ndarray, layer_goes_front: bool) -> np.ndarray:
	new_layer = np.stack([np.zeros_like(a[:, :, 0, :])], axis=2)
	if layer_goes_front:
		return np.concatenate([new_layer, a], axis=2)
	else:
		return np.concatenate([a, new_layer], axis=2)


def add_phase(a: np.ndarray, phase_goes_front: bool) -> np.ndarray:
	new_phase = np.stack([np.zeros_like(a[:, :, :, 0])], axis=3)
	if phase_goes_front:
		return np.concatenate([new_phase, a], axis=3)
	else:
		return np.concatenate([a, new_phase], axis=3)


def expand_all_directions(a: np.ndarray) -> np.ndarray:
	a = add_row(a, True)
	a = add_row(a, False)
	a = add_col(a, True)
	a = add_col(a, False)
	a = add_layer(a, True)
	a = add_layer(a, False)
	a = add_phase(a, True)
	a = add_phase(a, False)
	return a


def trim_array(a: np.ndarray) -> np.ndarray:
	while np.count_nonzero(a[0, :, :, :]) == 0:
		a = a[1:, :, :, :]
	while np.count_nonzero(a[-1, :, :, :]) == 0:
		a = a[:-1, :, :, :]
	while np.count_nonzero(a[:, 0, :, :]) == 0:
		a = a[:, 1:, :, :]
	while np.count_nonzero(a[:, -1, :, :]) == 0:
		a = a[:, :-1, :, :]
	while np.count_nonzero(a[:, :, 0, :]) == 0:
		a = a[:, :, 1:, :]
	while np.count_nonzero(a[:, :, -1, :]) == 0:
		a = a[:, :, :-1, :]
	while np.count_nonzero(a[:, :, :, 0]) == 0:
		a = a[:, :, :, 1:]
	while np.count_nonzero(a[:, :, :, -1]) == 0:
		a = a[:, :, :, :-1]
	return a


def apply_time_step(a: np.ndarray) -> np.ndarray:
	a = expand_all_directions(a)
	new_a = np.empty_like(a)
	for i in range(a.shape[0]):
		for j in range(a.shape[1]):
			for k in range(a.shape[2]):
				for l in range(a.shape[3]):
					neighbor_count = 0
					for i_shift in SHIFTS:
						new_i = i + i_shift
						if not (0 <= new_i < a.shape[0]):
							continue  # don't go out of range
						for j_shift in SHIFTS:
							new_j = j + j_shift
							if not (0 <= new_j < a.shape[1]):
								continue  # don't go out of range
							for k_shift in SHIFTS:
								new_k = k + k_shift
								if not (0 <= new_k < a.shape[2]):
									continue  # don't go out of range
								for l_shift in SHIFTS:
									new_l = l + l_shift
									if not (0 <= new_l < a.shape[3]):
										continue  # don't go out of range
									if i_shift == 0 and j_shift == 0 and k_shift == 0 and l_shift == 0:
										continue  # don't count the center
									if a[new_i, new_j, new_k, new_l]:
										neighbor_count += 1
					if a[i, j, k, l]:
						new_a[i, j, k, l] = (neighbor_count == 2 or neighbor_count == 3)
					else:
						new_a[i, j, k, l] = (neighbor_count == 3)
	return trim_array(new_a)


if __name__ == "__main__":
	cubes_configuration = read_input_file()
	for _ in range(6):
		cubes_configuration = apply_time_step(cubes_configuration)
	active_count = np.count_nonzero(cubes_configuration)
	print(f"number of active cubes after 6 cycles: {active_count}")
