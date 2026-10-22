import json


def read_amount():
	while True:
		try:
			num = float(input("Введите сумму затраты: "))
		except ValueError:
			print("Введите число, например 150000!")
		else:
			if num > 0:
				return num
			else:
				print("Сумма должна быть больше нуля")


def show_expenses(expenses):
	total = 0

	for expense in expenses:
		print(expense["name"], expense["amount"])
		total = total + expense["amount"]

	print("Количество расходов:", len(expenses))
	print("Всего потрачено:", total)


def load_expenses():
	try:
		with open("expenses.json", "r", encoding="utf-8") as file:
			return json.load(file)
	except FileNotFoundError:
		return []


def save_expenses(expenses):
	with open("expenses.json", "w", encoding="utf-8") as file:
		json.dump(expenses, file, ensure_ascii=False, indent=4)


expenses = load_expenses()

while True:
	print("\n1. Добавить расход")
	print("2. Показать расходы")
	print("0. Выйти")

	choice = input("Выберите действие: ").strip()

	if choice == "1":
		name = input("На что потратились: ").strip()

		if not name:
			print("Название не должно быть пустым")
			continue

		num = read_amount()
		expenses.append({"name": name, "amount": num})
		save_expenses(expenses)
		print("Расход сохранён:", name, num)

	elif choice == "2":
		show_expenses(expenses)

	elif choice == "0":
		print("До свидания!")
		break

	else:
		print("Неизвестная команда. Введите 1, 2 или 0.")