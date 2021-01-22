import re
from typing import List, Tuple
from constants import UTF_8


INPUT_FILE_NAME = "passwords.txt"
PASSWORD_LINE_RE = re.compile(r"([0-9]+)-([0-9]+) (.): (.*)")


def read_password_file() -> List[Tuple[int, int, str, str]]:
	to_return = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line_ in in_file:
			line = line_.strip()
			match = PASSWORD_LINE_RE.fullmatch(line)
			num1_str = match.group(1)
			num1 = int(num1_str)
			num2_str = match.group(2)
			num2 = int(num2_str)
			c = match.group(3)
			password = match.group(4)
			to_return.append((num1, num2, c, password))
	return to_return


def count_valid_passwords1(password_info: List[Tuple[int, int, str, str]]) -> int:
	count = 0
	for min_num, max_num, c, password in password_info:
		this_count = 0
		for c2 in password:
			if c2 == c:
				this_count += 1
				if this_count > max_num:
					break
		if min_num <= this_count <= max_num:
			count += 1
	return count


def count_valid_passwords2(password_info: List[Tuple[int, int, str, str]]) -> int:
	count = 0
	for num1, num2, c, password in password_info:
		this_count = 0
		for num in [num1, num2]:
			if password[num - 1] == c:
				this_count += 1
		if this_count == 1:
			count += 1
	return count


if __name__ == "__main__":
	p_word_info = read_password_file()
	valid_count = count_valid_passwords1(p_word_info)
	print(f"Valid passwords: {valid_count}")
	valid_count = count_valid_passwords2(p_word_info)
	print(f"Valid passwords: {valid_count}")
