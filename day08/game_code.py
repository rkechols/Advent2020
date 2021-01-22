from typing import List, Tuple, Union
from constants import UTF_8


INPUT_FILE_NAME = "game_code.txt"
ACCUMULATE = "acc"
JUMP = "jmp"
NO_OPERATION = "nop"


def read_input_file() -> List[Tuple[str, int]]:
	to_return = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			space_index = line.find(" ")
			command_str = line[:space_index]
			num_str = line[(space_index + 1):]
			num = int(num_str)
			to_return.append((command_str, num))
	return to_return


def execute_commands_no_loop(commands: List[Tuple[str, int]]) -> Union[None, int]:
	accumulator = 0
	next_command_index = 0
	used_commands = set()
	while next_command_index not in used_commands:
		if next_command_index == len(commands):
			# we successfully finished the program
			return accumulator
		used_commands.add(next_command_index)
		command, num = commands[next_command_index]
		if command == ACCUMULATE:
			accumulator += num
			next_command_index += 1
		elif command == JUMP:
			next_command_index += num
		elif command == NO_OPERATION:
			next_command_index += 1
		else:
			raise ValueError(f"UNKNOWN COMMAND - line {next_command_index}: {command} {num}")
	return None  # the while loop closed, meaning we tried to repeat a command


def find_problem(commands: List[Tuple[str, int]]) -> int:
	for i in range(len(commands)):
		original = commands[i][0]
		if original == ACCUMULATE:
			continue
		if original == NO_OPERATION:
			new_commands = commands[:i] + [(JUMP, commands[i][1])] + commands[(i + 1):]
		elif original == JUMP:
			new_commands = commands[:i] + [(NO_OPERATION, commands[i][1])] + commands[(i + 1):]
		else:
			raise ValueError(f"UNKNOWN COMMAND - line {i}: {commands[i][0]} {commands[i][1]}")
		val = execute_commands_no_loop(new_commands)
		if val is not None:
			return val
	raise ValueError("NO ANSWER")


if __name__ == "__main__":
	command_list = read_input_file()
	print(find_problem(command_list))
