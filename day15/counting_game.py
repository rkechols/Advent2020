from typing import List
from constants import UTF_8


INPUT_FILE_NAME = "counting_numbers.txt"


def read_input_file() -> List[int]:
	starting_numbers = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			starting_numbers += [int(x) for x in line.strip().split(",")]
	return starting_numbers


def count_numbers(starting_numbers: List[int], target: int) -> int:
	history = dict()
	# initialize
	for i, number in enumerate(starting_numbers[:-1], start=1):
		if i == target:
			return number
		history[number] = i
	current_number = starting_numbers[-1]
	index = len(starting_numbers)
	while index < target:
		if current_number in history:
			next_number = index - history[current_number]
		else:
			next_number = 0
		history[current_number] = index
		index += 1
		current_number = next_number
	return current_number


if __name__ == "__main__":
	numbers = read_input_file()
	target_number = count_numbers(numbers, 2020)
	print("the 2020th number:", target_number)
	target_number = count_numbers(numbers, 30000000)
	print("the 30000000th number:", target_number)
