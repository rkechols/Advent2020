from typing import Tuple
from constants import UTF_8


INPUT_FILE_NAME = "public_keys.txt"


SUBJECT_NUMBER_INITIAL = 7
DIVIDE_NUMBER = 20201227


def read_input_file() -> Tuple[int, int]:
	public_keys = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			public_keys.append(int(line.strip()))
	if len(public_keys) != 2:
		raise ValueError("didn't find exactly 2 public keys")
	return public_keys[0], public_keys[1]


def transform_subject(subject_number: int, loop_size: int) -> int:
	value = 1
	for _ in range(loop_size):
		value *= subject_number
		value %= DIVIDE_NUMBER
	return value


def get_loop_size(public_key: int) -> int:
	# find a value that gets us the public key
	n = 0
	running_value = 1
	while True:
		if running_value == public_key:
			return n
		running_value = (running_value * SUBJECT_NUMBER_INITIAL) % DIVIDE_NUMBER
		n += 1


if __name__ == "__main__":
	public_key1, public_key2 = read_input_file()
	loop_size1 = get_loop_size(public_key1)
	print(f"loop_size 1: {loop_size1}")
	encryption_key1 = transform_subject(public_key2, loop_size1)
	print(f"encryption key 1: {encryption_key1}")
	loop_size2 = get_loop_size(public_key2)
	print(f"loop_size 2: {loop_size2}")
	encryption_key2 = transform_subject(public_key1, loop_size2)
	print(f"encryption key 2: {encryption_key2}")
