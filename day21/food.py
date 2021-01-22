import re
from typing import List, Tuple, Set, Dict
from constants import UTF_8


INPUT_FILE_NAME = "ingredients_allergens.txt"

INPUT_LINE_RE = re.compile(r"(.*) \(contains (.*)\)")


def read_input_file() -> List[Tuple[Set[str], Set[str]]]:
	food_info = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			match = INPUT_LINE_RE.fullmatch(line.strip())
			ingredients = set(match.group(1).split(" "))
			allergens = set(match.group(2).split(", "))
			food_info.append((ingredients, allergens))
	return food_info


def collect_ingredients_and_allergens(food_info: List[Tuple[Set[str], Set[str]]]) -> Tuple[Set[str], Set[str]]:
	ingredients = set()
	allergens = set()
	for these_ingredients, these_allergens in food_info:
		ingredients.update(these_ingredients)
		allergens.update(these_allergens)
	return ingredients, allergens


def find_containing_ingredients(food_info: List[Tuple[Set[str], Set[str]]], allergens: Set[str]) -> Dict[str, str]:
	# make a space to record possible containing ingredients for each allergen
	allergen_to_ingredients = dict()
	for allergen in allergens:
		allergen_to_ingredients[allergen] = set()
	# initialize
	for ingredients, these_allergens in food_info:
		# each allergen listed for this food could be caused by any of the ingredients
		for allergen in these_allergens:
			allergen_to_ingredients[allergen].update(ingredients)
	# narrow down the options
	for allergen in allergens:
		# every time this allergen is present, there has to be at least one common ingredient causing it each time
		for ingredients, these_allergens in food_info:
			if allergen in these_allergens:
				allergen_to_ingredients[allergen].intersection_update(ingredients)
	# if we've figured out what ingredient contains a specific allergen, it can't contain any other allergens
	to_return = dict()
	made_change = True
	while made_change:
		made_change = False
		for allergen, ingredients in allergen_to_ingredients.items():
			if len(ingredients) == 1:
				problem_ingredient = list(ingredients)[0]
				to_return[allergen] = problem_ingredient
				for other_allergen in allergens:
					if other_allergen == allergen:
						continue  # skip the allergen that got us this new info and has only the 1 ingredient
					if problem_ingredient in allergen_to_ingredients[other_allergen]:
						allergen_to_ingredients[other_allergen].remove(problem_ingredient)
						made_change = True
	if max((len(options) for options in allergen_to_ingredients.values())) != 1:
		raise ValueError("sorry, couldn't narrow it down to one causing ingredient for each allergen")
	return to_return


def count_ingredient_appearances(target_ingredients: Set[str], food_info: List[Tuple[Set[str], Set[str]]]) -> int:
	count = 0
	for ingredients, _ in food_info:
		for ingredient in ingredients:
			if ingredient in target_ingredients:
				count += 1
	return count


if __name__ == "__main__":
	all_food_info = read_input_file()
	all_ingredients, all_allergens = collect_ingredients_and_allergens(all_food_info)
	allergen_to_ingredient = find_containing_ingredients(all_food_info, all_allergens)
	non_problem_ingredients = all_ingredients.difference(set(allergen_to_ingredient.values()))
	non_problem_count = count_ingredient_appearances(non_problem_ingredients, all_food_info)
	print(f"appearance count of non-problem ingredients: {non_problem_count}")
	sorted_problem_ingredients = list()
	for allergen_ in sorted(allergen_to_ingredient):
		sorted_problem_ingredients.append(allergen_to_ingredient[allergen_])
	print("canonical dangerous ingredient list:")
	print(",".join(sorted_problem_ingredients))
