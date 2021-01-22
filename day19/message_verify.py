import copy
import re
from typing import List, Tuple, Dict, Set
from constants import UTF_8


INPUT_FILE_NAME = "messages.txt"

START_SYMBOL = "0"


def read_input_file() -> Tuple[Dict[str, List[List[str]]], List[str]]:
	rules = dict()
	messages = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		doing_rules = True
		for line_ in in_file:
			line = line_.strip()
			if line == "":  # there's a blank line that switches from rules to input
				doing_rules = False
				continue
			# read and save the rules
			if doing_rules:
				i = 0
				while line[i] != ":":
					i += 1
				rule_number = line[:i]
				rules[rule_number] = list()
				options = line[(i + 1):].strip().split("|")
				for option in options:
					symbols = list()
					for symbol in option.strip().split(" "):
						if symbol[0] == '"':
							# strip quotes from terminals
							symbols.append(symbol[1:-1])
						else:
							symbols.append(symbol)
					rules[rule_number].append(symbols)
			# read and save the input strings
			else:
				messages.append(line)
	return rules, messages


def build_symbol_regex(symbol: str, rules: Dict[str, List[List[str]]], regex_cache: Dict[str, str]) -> str:
	# we've already built a regex for this symbol
	if symbol in regex_cache:
		return regex_cache[symbol]
	# it's a terminal
	if symbol not in rules:
		regex_cache[symbol] = symbol
		return symbol
	# it's a non-terminal
	option_regexes = list()
	for option in rules[symbol]:
		option_regex = "".join([build_symbol_regex(s, rules, regex_cache) for s in option])
		option_regexes.append(option_regex)
	n = len(option_regexes)
	if n == 0:
		raise ValueError("No options?")
	elif n > 1:
		this_regex = "(?:" + "|".join(option_regexes) + ")"
	else:  # n == 1
		this_regex = option_regexes[0]
	regex_cache[symbol] = this_regex
	return this_regex


def dfs_for_first_set(symbol: str, rules: Dict[str, List[List[str]]], first_sets: Dict[str, Set[str]]):
	if symbol in first_sets:
		# we already have this one's first set
		return
	if symbol not in rules:
		# it's a terminal
		first_sets[symbol] = {symbol}
		return
	# it's a non-terminal we haven't calculated yet
	# its first set is the union of all of the first sets of the first symbol of each production
	this_first_set = set()
	for option in rules[symbol]:
		first_symbol = option[0]
		dfs_for_first_set(first_symbol, rules, first_sets)
		for x in first_sets[first_symbol]:
			this_first_set.add(x)
	first_sets[symbol] = this_first_set


def build_first_sets(rules: Dict[str, List[List[str]]]) -> Dict[str, Set[str]]:
	first_sets = dict()
	for non_terminal in rules:
		dfs_for_first_set(non_terminal, rules, first_sets)
	return first_sets


def check(message: str, rules: Dict[str, List[List[str]]], first_sets: Dict[str, Set[str]], i: int, stack: List[str]) -> int:
	n = len(message)
	while len(stack) > 0:
		symbol = stack.pop()
		if symbol not in rules:  # it's a terminal
			if message[i] != symbol:  # mismatch!
				return -1
			# it matches, advance the input cursor
			i += 1
			if i == n and len(stack) != 0:
				return -1
		else:  # it's a non-terminal
			valid_options = list()
			for option in rules[symbol]:
				if message[i] in first_sets[option[0]]:
					valid_options.append(option)
			num_valid_options = len(valid_options)
			if num_valid_options == 0:  # no valid options; game over
				return -1
			elif num_valid_options == 1:  # exactly one way to go; don't branch recursively
				for s in reversed(valid_options[0]):
					stack.append(s)
			else:  # multiple options; we need to try them all
				for option in valid_options:
					new_stack = copy.copy(stack)
					for s in reversed(option):
						new_stack.append(s)
					new_i = check(message, rules, first_sets, i, new_stack)
					if new_i == n and len(new_stack) == 0:  # we did it!
						stack.clear()
						return new_i
				# none of the options worked
				return -1
	return i


def message_is_valid(message: str, rules: Dict[str, List[List[str]]], first_sets: Dict[str, Set[str]]) -> bool:
	stack = [START_SYMBOL]
	cursor_index = check(message, rules, first_sets, 0, stack)
	if cursor_index != len(message):
		# either we got a -1 because something didn't match, or we didn't make it through all of the input
		return False
	elif len(stack) != 0:
		# we ran out of input, but there was still something on the stack
		return False
	else:  # things line up
		return True


if __name__ == "__main__":
	rules_dict, messages_list = read_input_file()
	regex_dict = dict()
	start_symbol_re_str = build_symbol_regex(START_SYMBOL, rules_dict, regex_dict)
	start_symbol_re = re.compile(start_symbol_re_str)
	count = 0
	for m in messages_list:
		if start_symbol_re.fullmatch(m) is not None:
			count += 1
	print(f"PART 1 - regex:  number of valid messages: {count}")
	first_sets_dict = build_first_sets(rules_dict)
	count = 0
	for m in messages_list:
		if message_is_valid(m, rules_dict, first_sets_dict):
			count += 1
	print(f"PART 1 - parser: number of valid messages: {count}")
	# for part 2, we modify rules 8 and 11
	rules_dict["8"].append(["42", "8"])
	rules_dict["11"].append(["42", "11", "31"])
	count = 0
	for m in messages_list:
		if message_is_valid(m, rules_dict, first_sets_dict):
			count += 1
	print(f"PART 2 - parser: number of valid messages: {count}")
