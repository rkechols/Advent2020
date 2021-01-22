from typing import List
from constants import UTF_8


INPUT_FILE_NAME = "math_homework.txt"

DIGITS = "0123456789"
PLUS = "+"
PLUS_SUBSTITUTE = "$"
TIMES = "*"
PAREN_L = "("
PAREN_R = ")"


def read_input_file() -> List[str]:
	expressions = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			expressions.append(line.replace(" ", "").strip())
	return expressions


def evaluate_expression_basic(expression: str) -> int:
	stack = list()
	for c in expression:
		if c == TIMES or c == PLUS or c == PAREN_L:
			stack.append(c)
		elif c in DIGITS:
			this_num = int(c)
			if len(stack) == 0 or stack[-1] == PAREN_L:
				stack.append(c)
			elif stack[-1] == PLUS:
				stack.pop()  # remove the plus
				prev_num = int(stack.pop())  # get the other value to add
				stack.append(str(prev_num + this_num))
			elif stack[-1] == TIMES:
				stack.pop()  # remove the star
				prev_num = int(stack.pop())  # get the other value to multiply
				stack.append(str(prev_num * this_num))
		elif c == PAREN_R:
			this_num = int(stack.pop())
			stack.pop()  # remove the opening paren
			if len(stack) == 0 or stack[-1] == PAREN_L:
				stack.append(str(this_num))
			else:
				op = stack.pop()  # get the previous operator
				prev_num = int(stack.pop())
				if op == PLUS:
					stack.append(str(prev_num + this_num))
				elif op == TIMES:
					stack.append(str(prev_num * this_num))
				else:
					raise ValueError(f"Unexpected operator: {op}")
		else:
			raise ValueError(f"Unknown symbol: {c}")
	if len(stack) != 1:
		raise ValueError(f"Stack was not size 1 when the evaluation finished!")
	return int(stack.pop())


def add_plus_precedence(expression: str) -> str:
	# convert all plus signs to a new substitute operator
	expression = expression.replace(PLUS, PLUS_SUBSTITUTE)
	# while there's still any instance of the substitute, replace it with a plus that has the correct parenthesis
	while True:
		operator_index = expression.find(PLUS_SUBSTITUTE)
		if operator_index == -1:
			break  # no more substitute operators to replace
		# find the left edge of the left operand
		left_edge = operator_index - 1
		if left_edge < 0:
			raise ValueError("Went out of bounds looking for left edge of left operand! (immediately)")
		if expression[left_edge] not in DIGITS:
			paren_count = 0
			found_edge = False
			while left_edge >= 0:
				c = expression[left_edge]
				if c == PAREN_R:
					paren_count += 1
				elif c == PAREN_L:
					paren_count -= 1
					if paren_count == 0:
						found_edge = True
						break
				left_edge -= 1
			if not found_edge:
				raise ValueError("Went out of bounds looking for left edge of left operand!")
		# find the right edge of the right operand
		n = len(expression)
		right_edge = operator_index + 1
		if right_edge >= n:
			raise ValueError("Went out of bounds looking for right edge of right operand! (immediately)")
		if expression[right_edge] not in DIGITS:
			paren_count = 0
			found_edge = False
			while right_edge < n:
				c = expression[right_edge]
				if c == PAREN_L:
					paren_count += 1
				elif c == PAREN_R:
					paren_count -= 1
					if paren_count == 0:
						found_edge = True
						break
				right_edge += 1
			if not found_edge:
				raise ValueError("Went out of bounds looking for right edge of right operand!")
		# because we want the break on the right hand side of that last character we just found
		# and the right end of a string slice is exclusive, we need to add one more
		right_edge += 1
		# put parenthesis around this chunk and swap to operator back to a normal plus
		before = expression[:left_edge]
		left_operand = expression[left_edge:operator_index]
		right_operand = expression[(operator_index + 1):right_edge]
		after = expression[right_edge:]
		expression = before + PAREN_L + left_operand + PLUS + right_operand + PAREN_R + after
	return expression


def evaluate_expression_advanced(expression: str) -> int:
	expression = add_plus_precedence(expression)
	return evaluate_expression_basic(expression)


if __name__ == "__main__":
	expressions_list = read_input_file()
	total = 0
	for expr in expressions_list:
		total += evaluate_expression_basic(expr)
	print(f"BASIC: sum of all expression values: {total}")
	total = 0
	for expr in expressions_list:
		total += evaluate_expression_advanced(expr)
	print(f"ADVANCED: sum of all expression values: {total}")
