from constants import UTF_8


INPUT_FILE_NAME = "expense_report.txt"
TARGET = 2020


def two_numbers():
	print("TWO NUMBERS:")
	all_numbers = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			number_str = line.strip()
			number = int(number_str)
			for previous_number in all_numbers:
				if previous_number + number == TARGET:
					print(previous_number * number)
					return
			all_numbers.append(number)
	print("NO ANSWER")


def three_numbers():
	print("THREE NUMBERS:")
	all_numbers = list()
	with open(INPUT_FILE_NAME, "r", encoding=UTF_8) as in_file:
		for line in in_file:
			number_str = line.strip()
			number = int(number_str)
			all_numbers.append(number)
	n = len(all_numbers)
	for i in range(n):
		number_i = all_numbers[i]
		if number_i > TARGET:
			continue
		for j in range(i, n):
			number_j = all_numbers[j]
			if number_i + number_j > TARGET:
				continue
			for k in range(j, n):
				number_k = all_numbers[k]
				if number_i + number_j + number_k == TARGET:
					print(number_i * number_j * number_k)
					return
	print("NO ANSWER")


if __name__ == "__main__":
	two_numbers()
	three_numbers()
