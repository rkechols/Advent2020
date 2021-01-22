from typing import List, Tuple
from constants import UTF_8


INPUT_FILE_NAME = "ferry_directions.txt"


class Boat:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.waypoint_x = 10
		self.waypoint_y = 1

	def north(self, delta: int):
		self.waypoint_y += delta

	def south(self, delta: int):
		self.waypoint_y -= delta

	def east(self, delta: int):
		self.waypoint_x += delta

	def west(self, delta: int):
		self.waypoint_x -= delta

	def left(self, theta_delta: int):
		if theta_delta == 180:
			self.waypoint_x *= -1
			self.waypoint_y *= -1
		elif theta_delta == 90:
			self.waypoint_x, self.waypoint_y = -self.waypoint_y, self.waypoint_x
		elif theta_delta == 270:
			self.waypoint_x, self.waypoint_y = self.waypoint_y, -self.waypoint_x

	def right(self, theta_delta: int):
		self.left(360 - theta_delta)

	def forward(self, steps: int):
		self.x += steps * self.waypoint_x
		self.y += steps * self.waypoint_y


def read_input_file() -> List[Tuple[str, int]]:
	instructions = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line_ in in_file:
			line = line_.strip()
			action_str = line[0]
			action_number = int(line[1:])
			instructions.append((action_str, action_number))
	return instructions


def follow_instruction(action: str, value: int, boat: Boat):
	if action == "N":
		boat.north(value)
	elif action == "S":
		boat.south(value)
	elif action == "E":
		boat.east(value)
	elif action == "W":
		boat.west(value)
	elif action == "L":
		boat.left(value)
	elif action == "R":
		boat.right(value)
	elif action == "F":
		boat.forward(value)
	else:
		raise ValueError(f"Unknown action type: {action}")
	return


if __name__ == "__main__":
	all_instructions = read_input_file()
	b = Boat()
	for a_str, a_num in all_instructions:
		follow_instruction(a_str, a_num, b)
	print(f"boat ending location: ({b.x},{b.y})")
	print(f"manhattan distance from origin:", abs(b.x) + abs(b.y))
