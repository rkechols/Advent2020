import copy
from typing import List, Tuple
from constants import UTF_8


INPUT_FILE_NAME = "cards.txt"


def read_input_file() -> Tuple[List[int], List[int]]:
	p1_cards = list()
	p2_cards = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		is_player_1 = False
		for line_ in in_file:
			if line_.startswith("Player"):
				is_player_1 = not is_player_1
			else:
				line = line_.strip()
				if line != "":
					if is_player_1:
						p1_cards.append(int(line))
					else:
						p2_cards.append(int(line))
	return p1_cards, p2_cards


def calculate_score(hand: List[int]) -> int:
	n = len(hand)
	total = 0
	for i, card_value in enumerate(hand):
		total += (n - i) * card_value
	return total


def play_combat(p1_cards: List[int], p2_cards: List[int]) -> int:
	p1_cards = copy.copy(p1_cards)
	p2_cards = copy.copy(p2_cards)
	while len(p1_cards) != 0 and len(p2_cards) != 0:
		# list start = top of the deck/hand
		p1_card = p1_cards.pop(0)
		p2_card = p2_cards.pop(0)
		if p1_card > p2_card:
			p1_cards.append(p1_card)
			p1_cards.append(p2_card)
		elif p2_card > p1_card:
			p2_cards.append(p2_card)
			p2_cards.append(p1_card)
		else:
			raise ValueError("there was a tie...?")
	if len(p1_cards) > 0:
		print("player 1 wins")
		return calculate_score(p1_cards)
	else:
		print("player 2 wins")
		return calculate_score(p2_cards)


def play_recursive_combat(p1_cards: List[int], p2_cards: List[int]) -> bool:
	used_configurations = set()
	while len(p1_cards) != 0 and len(p2_cards) != 0:
		this_configuration = str(p1_cards) + str(p2_cards)
		if this_configuration in used_configurations:
			return True
		used_configurations.add(this_configuration)
		# list start = top of the deck/hand
		p1_card = p1_cards.pop(0)
		p2_card = p2_cards.pop(0)
		if len(p1_cards) >= p1_card and len(p2_cards) >= p2_card:
			# new game of recursive combat
			p1_wins_round = play_recursive_combat(p1_cards[:p1_card], p2_cards[:p2_card])
		else:
			# can't recurse: player with the bigger card wins the round
			p1_wins_round = p1_card > p2_card
		if p1_wins_round:
			p1_cards.append(p1_card)
			p1_cards.append(p2_card)
		else:
			p2_cards.append(p2_card)
			p2_cards.append(p1_card)
	return len(p1_cards) > 0


def play_recursive_combat_main(p1_cards: List[int], p2_cards: List[int]) -> int:
	p1_cards = copy.copy(p1_cards)
	p2_cards = copy.copy(p2_cards)
	p1_wins = play_recursive_combat(p1_cards, p2_cards)
	if p1_wins:
		print("player 1 wins")
		return calculate_score(p1_cards)
	else:
		print("player 2 wins")
		return calculate_score(p2_cards)


if __name__ == "__main__":
	player1_cards, player2_cards = read_input_file()
	print("REGULAR GAME")
	score = play_combat(player1_cards, player2_cards)
	print(f"score of the winning player: {score}")
	print("----------")
	print("RECURSIVE GAME")
	score = play_recursive_combat_main(player1_cards, player2_cards)
	print(f"score of the winning player: {score}")
