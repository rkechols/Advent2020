from typing import Dict, List, Tuple
from constants import UTF_8


INPUT_FILE_NAME = "busses.txt"
BUS_X = -1


def read_input_file() -> Tuple[int, List[int]]:
	busses = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		start_time = int(in_file.readline().strip())
		for other_num in in_file.readline().strip().split(","):
			if other_num == "x":
				busses.append(BUS_X)
			else:
				busses.append(int(other_num))
	return start_time, busses


def find_first_bus(start_time: int, busses: List[int]) -> Tuple[int, int]:
	lowest_wait_time = max(busses)
	best_selected_bus = -1
	for bus_id in busses:
		if bus_id == BUS_X:
			continue
		if start_time % bus_id == 0:
			return 0, bus_id
		finished_repetitions = start_time // bus_id
		most_recent_passing = bus_id * finished_repetitions
		next_passing = most_recent_passing + bus_id
		this_wait_time = next_passing - start_time
		if this_wait_time < lowest_wait_time:
			lowest_wait_time = this_wait_time
			best_selected_bus = bus_id
	if best_selected_bus == -1:
		raise ValueError("ERROR: didn't find a bus that has me wait less than the largest bus ID number")
	return lowest_wait_time, best_selected_bus


def bus_list_to_offset_dict(busses: List[int]) -> Dict[int, int]:
	bus_offsets = dict()
	for i, bus_id in enumerate(busses):
		if bus_id != BUS_X:
			bus_offsets[bus_id] = i
	return bus_offsets


def time_is_aligned(t: int, bus_offsets: Dict[int, int]) -> bool:
	for bus_id, offset in bus_offsets.items():
		if (t + offset) % bus_id != 0:
			return False
	return True


def find_first_synchronized_time(bus_offsets: Dict[int, int]) -> int:
	bus_ids_sorted = list(bus_offsets.keys())
	bus_ids_sorted.sort(reverse=True)
	step = 1
	next_bus_index = 0
	next_bus_id = bus_ids_sorted[next_bus_index]
	time_to_check = 0
	while next_bus_index < len(bus_ids_sorted):
		if time_is_aligned(time_to_check, bus_offsets):
			return time_to_check
		if (time_to_check + bus_offsets[next_bus_id]) % next_bus_id == 0:
			step *= next_bus_id
			next_bus_index += 1
			next_bus_id = bus_ids_sorted[next_bus_index]
		time_to_check += step
	raise ValueError("NO ANSWER")


if __name__ == "__main__":
	start_time_available, bus_list = read_input_file()
	time_to_wait, bus_to_catch = find_first_bus(start_time_available, bus_list)
	print(f"next available bus is #{bus_to_catch}, after waiting {time_to_wait} time steps")
	print(f"the product of those numbers is {bus_to_catch * time_to_wait}")
	bus_offset_dict = bus_list_to_offset_dict(bus_list)
	synchronized_time = find_first_synchronized_time(bus_offset_dict)
	print(f"first timestep that has everything synchronized: {synchronized_time}")
