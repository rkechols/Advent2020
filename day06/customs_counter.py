from typing import List
from constants import UTF_8


INPUT_FILE_NAME = "customs_declarations.txt"


def read_input_file() -> List[List[str]]:
	all_lines = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			all_lines.append(line)
	file_contents = "".join(all_lines)
	group_declarations = file_contents.split("\n\n")
	return [group_declaration.split("\n") for group_declaration in group_declarations]


def count_declarations(group_declarations_: List[str]) -> int:
	group_declarations = list()
	for s in group_declarations_:
		if s != "":
			group_declarations.append(s)
	letters = set()
	for c in group_declarations[0]:
		letters.add(c)
	for declaration in group_declarations[1:]:
		this_set = set()
		for c in declaration:
			this_set.add(c)
		letters = letters.intersection(this_set)
	return len(letters)


if __name__ == "__main__":
	all_groups = read_input_file()
	count = 0
	for group in all_groups:
		this_count = count_declarations(group)
		count += this_count
	print("sum of all group declarations:", count)
