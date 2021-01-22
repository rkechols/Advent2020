import re
from typing import Dict, List
from constants import UTF_8


INPUT_FILE_NAME = "port_initialization.txt"
BIT_COUNT = 36
MASK_PREFIX = "mask = "

MEM_COMMAND_RE = re.compile(r"mem\[([0-9]+)] = ([0-9]+)")


def read_input_file() -> List[str]:
	commands = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			commands.append(line.strip())
	return commands


def to_binary(num: int) -> str:
	remaining = num
	bits = list()
	for power in range(BIT_COUNT - 1, -1, -1):
		value = pow(2, power)
		if remaining - value >= 0:
			bits.append("1")
			remaining -= value
		else:
			bits.append("0")
	return "".join(bits)


def from_binary(num: str) -> int:
	total = 0
	for i, bit in enumerate(num):
		if bit == "0":
			continue
		power = (BIT_COUNT - 1) - i
		total += pow(2, power)
	return total


def apply_mask1(binary_number: str, mask: str) -> str:
	new_bits = list()
	for original_bit, mask_bit in zip(binary_number, mask):
		if mask_bit == "X":
			new_bits.append(original_bit)
		else:
			new_bits.append(mask_bit)
	return "".join(new_bits)


def interpret_commands1(commands: List[str]) -> Dict[int, int]:
	memory = dict()
	mask = ""
	for command in commands:
		if command.startswith(MASK_PREFIX):
			mask = command[len(MASK_PREFIX):]
			continue
		# else begins with 'mem'
		match = MEM_COMMAND_RE.fullmatch(command)
		address = int(match.group(1))
		value = int(match.group(2))
		value_binary = to_binary(value)
		value_binary = apply_mask1(value_binary, mask)
		value = from_binary(value_binary)
		memory[address] = value
	return memory


def apply_mask2(binary_number: str, mask: str) -> str:
	new_bits = list()
	for original_bit, mask_bit in zip(binary_number, mask):
		if mask_bit == "0":
			new_bits.append(original_bit)
		elif mask_bit == "1":
			new_bits.append("1")
		else:  # mask_bit == "X"
			new_bits.append(mask_bit)
	return "".join(new_bits)


def resolve_floating_binary(binary_number: str) -> List[str]:
	options = [binary_number]
	for i, bit in enumerate(binary_number):
		if bit == "X":
			new_options = list()
			for option in options:
				new_options.append(option[:i] + "0" + option[(i + 1):])
				new_options.append(option[:i] + "1" + option[(i + 1):])
			options = new_options
	return options


def interpret_commands2(commands: List[str]) -> Dict[int, int]:
	memory = dict()
	mask = ""
	for command in commands:
		if command.startswith(MASK_PREFIX):
			mask = command[len(MASK_PREFIX):]
			continue
		# else begins with 'mem'
		match = MEM_COMMAND_RE.fullmatch(command)
		address = int(match.group(1))
		value = int(match.group(2))
		address_binary = to_binary(address)
		address_binary_floating = apply_mask2(address_binary, mask)
		address_binary_list = resolve_floating_binary(address_binary_floating)
		for address_binary in address_binary_list:
			address = from_binary(address_binary)
			memory[address] = value
	return memory


if __name__ == "__main__":
	commands_list = read_input_file()
	memory_dict = interpret_commands1(commands_list)
	print(f"PART 1: sum of all values in memory: {sum(memory_dict.values())}")
	memory_dict = interpret_commands2(commands_list)
	print(f"PART 2: sum of all values in memory: {sum(memory_dict.values())}")
