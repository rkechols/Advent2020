import re
from typing import List, Tuple
from constants import UTF_8


INPUT_FILE_NAME = "train_tickets.txt"
FIELD_COUNT = 20

RULE_RE = re.compile(r"([^:]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)")
TARGET_PREFIX = "departure"


class Rule:
	def __init__(self, name: str, lower_range: Tuple[int, int], upper_range: Tuple[int, int]):
		self.name = name
		self.lower_range = lower_range
		self.upper_range = upper_range

	def value_is_valid(self, value: int) -> bool:
		in_lower = (self.lower_range[0] <= value <= self.lower_range[1])
		if in_lower:
			return True
		return self.upper_range[0] <= value <= self.upper_range[1]

	def __repr__(self) -> str:
		return f"{self.name}: {self.lower_range} or {self.upper_range}"


class Ticket:
	def __init__(self, values: List[int]):
		self.values = values

	def __iter__(self):
		for x in self.values:
			yield x

	def __getitem__(self, i: int) -> int:
		return self.values[i]

	def __repr__(self) -> str:
		return str(self.values)

	def __len__(self) -> int:
		return len(self.values)


def read_input_file() -> Tuple[List[Rule], Ticket, List[Ticket]]:
	rules = list()
	other_tickets = list()
	phase = 0
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line_ in in_file:
			line = line_.strip()
			if line == "":
				phase += 1
				continue
			if phase == 0:  # rules
				match = RULE_RE.fullmatch(line)
				name = match.group(1)
				lower_range = (int(match.group(2)), int(match.group(3)))
				upper_range = (int(match.group(4)), int(match.group(5)))
				rules.append(Rule(name, lower_range, upper_range))
			elif phase == 1:  # my ticket
				if line == "your ticket:":
					continue
				values = [int(x) for x in line.split(",")]
				my_ticket = Ticket(values)
			else:  # other tickets
				if line == "nearby tickets:":
					continue
				values = [int(x) for x in line.split(",")]
				other_tickets.append(Ticket(values))
	return rules, my_ticket, other_tickets


def filter_tickets(other_tickets: List[Ticket], rules: List[Rule]) -> List[Ticket]:
	valid_tickets = list()
	invalid_values = list()
	for ticket in other_tickets:
		has_invalid = False
		for value in ticket:
			is_valid = False
			for rule in rules:
				if rule.value_is_valid(value):
					is_valid = True
					break
			if not is_valid:
				has_invalid = True
				invalid_values.append(value)
				break
		if not has_invalid:
			valid_tickets.append(ticket)
	print(f"sum of all invalid values: {sum(invalid_values)}")
	return valid_tickets


def figure_field_order(other_tickets: List[Ticket], rules: List[Rule]) -> List[str]:
	# initialize options
	options = list()
	for i in range(FIELD_COUNT):
		these_options = set()
		for rule in rules:
			all_valid = True
			for ticket in other_tickets:
				if not rule.value_is_valid(ticket[i]):
					all_valid = False
			if all_valid:
				these_options.add(rule.name)
		options.append(these_options)
	# reduce all of the fields down to just one option
	finished_field_indices = set()
	while len(finished_field_indices) < FIELD_COUNT:
		found_new_fixed = False
		# look for slots that only have one option left
		for i, set_of_field_names in enumerate(options):
			if i in finished_field_indices:  # skip ones we already know about
				continue
			if len(set_of_field_names) == 1:  # we found one
				found_new_fixed = True
				for name in set_of_field_names:  # this happens exactly once
					finished_field_indices.add(i)
					for j in range(len(options)):  # remove it from all other slots
						if j != i:
							options[j].discard(name)
		# look for names that appear in only one slot
		for rule in rules:
			valid_slots = set()
			for i, set_of_field_names in enumerate(options):
				if rule.name in set_of_field_names:
					valid_slots.add(i)
			if len(valid_slots) == 1:
				slot_index = valid_slots.pop()
				if slot_index not in finished_field_indices:  # we found a new one
					found_new_fixed = True
					options[slot_index].clear()
					options[slot_index].add(rule.name)
		if not found_new_fixed:
			raise ValueError("stuck in infinite loop")
	return [set_of_field_names.pop() for set_of_field_names in options]


if __name__ == "__main__":
	rules_list, my_ticket_, other_tickets_list = read_input_file()
	other_tickets_list = filter_tickets(other_tickets_list, rules_list)
	field_order = figure_field_order(other_tickets_list, rules_list)
	product = None
	count = 0
	for i_, field_name in enumerate(field_order):
		if field_name.startswith(TARGET_PREFIX):
			count += 1
			if product is None:
				product = my_ticket_[i_]
			else:
				product *= my_ticket_[i_]
	if count != 6:
		print("DIDN'T FIND THE RIGHT NUMBER OF FIELDS WITH THE RIGHT PREFIX")
	print(f"product of the matching fields: {product}")
