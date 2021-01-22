import time
from typing import Dict, Tuple


STARTING_CUP_ORDER = "916438275"
SECTION_SIZE = 3
BIGGEST_CUP_NUMBER = 1000000
MOVE_COUNT = 10000000


def get_starting_cup_dict(big: bool) -> Tuple[Dict[int, int], int, int, int]:
	cups_list = [int(label) for label in STARTING_CUP_ORDER]
	biggest = max(cups_list)
	if big:
		cups_list += list(range(biggest + 1, BIGGEST_CUP_NUMBER + 1))
	n = len(cups_list)
	to_return = dict()
	for i in range(n):
		i_next = (i + 1) % n
		to_return[cups_list[i]] = cups_list[i_next]
	return to_return, cups_list[0], min(cups_list), max(cups_list)


def make_move(cups: Dict[int, int], current: int, lowest: int, highest: int) -> Tuple[Dict[int, int], int]:
	# take out the 3 cups
	temp = current
	removed = list()
	for _ in range(SECTION_SIZE):
		temp = cups[temp]
		removed.append(temp)
	first_after_removed = cups[temp]
	cups[current] = first_after_removed
	# figure out what cup we'll put them after
	# try "current - 1"
	destination_label = current - 1
	if destination_label < lowest:  # wrap to the highest label
		destination_label = highest
	while destination_label in removed:
		# not available; try the next one down
		destination_label -= 1
		if destination_label < lowest:  # wrap to the highest label
			destination_label = highest
	# put the 3 cups after the destination cup
	after_destination = cups[destination_label]
	cups[destination_label] = removed[0]
	cups[removed[-1]] = after_destination
	# return the cup after the current cup the new current cup
	return cups, cups[current]


if __name__ == "__main__":
	# part 1
	time_start = time.time()
	cup_circle, current_cup, low, high = get_starting_cup_dict(big=False)
	for _ in range(100):
		cup_circle, current_cup = make_move(cup_circle, current_cup, low, high)
	cup_circle_list = list()
	c = cup_circle[1]
	while c != 1:
		cup_circle_list.append(c)
		c = cup_circle[c]
	answer = "".join([str(c) for c in cup_circle_list])
	print(f"PART 1: order after 1: {answer}")
	time_end = time.time()
	print(f"time elapsed for part 1: {time_end - time_start} sec")
	print()
	# part 2
	time_start = time.time()
	cup_circle, current_cup, low, high = get_starting_cup_dict(big=True)
	for _ in range(MOVE_COUNT):
		cup_circle, current_cup = make_move(cup_circle, current_cup, low, high)
	after_1 = cup_circle[1]
	after_that = cup_circle[after_1]
	# this takes, like, 8 days. so, run it in Java?
	print(f"PART 2: product of 2 cup labels just after 1: {after_1 * after_that}")
	time_end = time.time()
	print(f"time elapsed for part 2: {time_end - time_start} sec")
