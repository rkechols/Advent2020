import re
from typing import List
from constants import UTF_8


INPUT_FILE_NAME = "passports.txt"

FIELD_VALUE_RE = re.compile(r"(\S*):(\S*)")
ALL_DIGITS = "0123456789"
ALL_HEX_CHARS = ALL_DIGITS + "abcdef"
ALL_EYE_COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


class Passport:
	def __init__(self, byr: str = None, iyr: int = None, eyr: int = None, hgt: str = None, hcl: str = None, ecl: str = None, pid: str = None, cid: str = None):
		if byr is None:
			self.byr = byr
		else:
			self.byr = int(byr)
		if iyr is None:
			self.iyr = iyr
		else:
			self.iyr = int(iyr)
		if eyr is None:
			self.eyr = eyr
		else:
			self.eyr = int(eyr)
		self.hgt = hgt
		self.hcl = hcl
		self.ecl = ecl
		self.pid = pid
		self.cid = cid

	def is_valid(self) -> bool:
		if self.byr is None:
			return False
		if not (1920 <= self.byr <= 2002):
			return False

		if self.iyr is None:
			return False
		if not (2010 <= self.iyr <= 2020):
			return False

		if self.eyr is None:
			return False
		if not (2020 <= self.eyr <= 2030):
			return False

		if self.hgt is None:
			return False
		if self.hgt.endswith("cm"):
			num_str = self.hgt[:-2]
			num = int(num_str)
			if not (150 <= num <= 193):
				return False
		elif self.hgt.endswith("in"):
			num_str = self.hgt[:-2]
			num = int(num_str)
			if not (59 <= num <= 76):
				return False
		else:
			return False

		if self.hcl is None:
			return False
		if len(self.hcl) == 0:
			return False
		if self.hcl[0] != "#":
			return False
		remaining = self.hcl[1:]
		if len(remaining) != 6:
			return False
		for c in remaining:
			if c not in ALL_HEX_CHARS:
				return False

		if self.ecl is None:
			return False
		if self.ecl not in ALL_EYE_COLORS:
			return False

		if self.pid is None:
			return False
		if len(self.pid) != 9:
			return False
		for c in self.pid:
			if c not in ALL_DIGITS:
				return False

		return True


def read_input_file() -> List[Passport]:
	all_lines = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			all_lines.append(line)
	file_contents = "".join(all_lines)
	passport_texts = file_contents.split("\n\n")
	passports = list()
	for passport_text in passport_texts:
		fields = dict()
		for match in FIELD_VALUE_RE.finditer(passport_text):
			field = match.group(1)
			value = match.group(2)
			fields[field] = value
		passports.append(Passport(**fields))
	return passports


if __name__ == "__main__":
	all_passports = read_input_file()
	valid_count = 0
	for p in all_passports:
		if p.is_valid():
			valid_count += 1
	print("valid passports:", valid_count)
