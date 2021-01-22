from typing import List
from constants import UTF_8


INPUT_FILE_NAME = "masking.txt"
WINDOW_LENGTH = 25


def read_input_file() -> List[int]:
	to_return = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line_ in in_file:
			line = line_.strip()
			to_return.append(int(line))
	return to_return


def is_paired_sum(target_sum: int, preceding_numbers: List[int]) -> bool:
	n = len(preceding_numbers)
	if n != WINDOW_LENGTH:
		raise ValueError("window not the right size! actual size:", n)
	for i in range(n - 1):
		for j in range(i + 1, n):
			if preceding_numbers[i] + preceding_numbers[j] == target_sum:
				return True
	return False


def find_contiguous_sum(target_sum: int, numbers: List[int]) -> List[int]:
	n = len(numbers)
	i = 0
	j = 1
	while True:
		chunk = numbers[i:j]
		s = sum(chunk)
		if s == target_sum:
			return chunk
		elif s < target_sum:
			j += 1
			if j > n:  # need more numbers, but there are none
				return list()
		else:  # s > target_sum
			i += 1
			if i > n:  # at the end of the list
				return list()


if __name__ == "__main__":
	number_list = read_input_file()
	for window_start in range(len(number_list) - (WINDOW_LENGTH + 1)):
		window_end = window_start + WINDOW_LENGTH
		target = number_list[window_end]
		if not is_paired_sum(target, number_list[window_start:window_end]):
			print("failed target:", target)
			contiguous_chunk = find_contiguous_sum(target, number_list)
			if len(contiguous_chunk) == 0:
				print("NO ANSWER")
			else:
				print("min + max:", min(contiguous_chunk) + max(contiguous_chunk))
			break
