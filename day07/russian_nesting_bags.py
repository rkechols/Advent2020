import re
from typing import Dict, Set, Tuple
from constants import UTF_8


INPUT_FILE_NAME = "bag_rules.txt"

FULL_BAG_RULE_RE = re.compile(r"(.*) bags contain (.*)\.")
ONE_COLOR_RE = re.compile(r"([0-9])+ (.*) bags?")
TARGET_COLOR = "shiny gold"


def read_input_file() -> Tuple[Dict[str, Dict[str, int]], Set[str]]:
	rules = dict()
	colors = set()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			full_line_match = FULL_BAG_RULE_RE.fullmatch(line.strip())
			this_color = full_line_match.group(1)
			colors.add(this_color)
			other_colors_str = full_line_match.group(2)
			inner_dict = dict()
			if other_colors_str != "no other bags":
				for color_block in other_colors_str.split(","):
					one_color_match = ONE_COLOR_RE.fullmatch(color_block.strip())
					count = int(one_color_match.group(1))
					other_color = one_color_match.group(2)
					colors.add(other_color)
					inner_dict[other_color] = count
			rules[this_color] = inner_dict
	return rules, colors


def build_containing_graph(rules: Dict[str, Dict[str, int]], colors: Set[str]) -> Dict[str, Set[str]]:
	graph = dict()
	for color in colors:
		graph[color] = set()
	for this_color, inner_colors in rules.items():
		for inner_color in inner_colors:
			graph[inner_color].add(this_color)
	return graph


def dfs(graph: Dict[str, Set[str]], to_visit: str, visited: Set[str]):
	if to_visit not in visited:
		visited.add(to_visit)
		for neighbor in graph[to_visit]:
			dfs(graph, neighbor, visited)


def count_containing_colors(source_color: str, graph: Dict[str, Set[str]]) -> int:
	visited = set()
	dfs(graph, source_color, visited)
	return len(visited) - 1


def count_inner_bags(source_color: str, rules: Dict[str, Dict[str, int]]) -> int:
	inner_count = 0
	for inner_color, count in rules[source_color].items():
		deeper_count = count_inner_bags(inner_color, rules)
		inner_count += (count + count * deeper_count)
	return inner_count


if __name__ == "__main__":
	rules_dict, colors_set = read_input_file()
	containing_graph = build_containing_graph(rules_dict, colors_set)
	print(f"number of colors that can contain {TARGET_COLOR}:", count_containing_colors(TARGET_COLOR, containing_graph))
	print(f"number of bags inside the {TARGET_COLOR} bag:", count_inner_bags(TARGET_COLOR, rules_dict))

