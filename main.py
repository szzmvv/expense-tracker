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
	if not expenses:
		print("Расходов пока нет.")
		return

	total = 0

	for number, expense in enumerate(expenses, start=1):
		print(number, expense["name"], expense["amount"])
		total = total + expense["amount"]

	print("Количество расходов:", len(expenses))
	print("Всего потрачено:", total)


def load_expenses():
	try:
		with open("expenses.json", "r", encoding="utf-8") as file:
			return json.load(file)
	except FileNotFoundError:
		return []
	except json.JSONDecodeError:
		print("Не удалось прочитать expenses.json: повреждён формат JSON.")
		print("Файл не изменён. Исправьте его перед запуском.")
		raise SystemExit(1)


def save_expenses(expenses):
	with open("expenses.json", "w", encoding="utf-8") as file:
		json.dump(expenses, file, ensure_ascii=False, indent=4)


def delete_expense(expenses):
	if not expenses:
		print("Список расходов пуст")
		return

	show_expenses(expenses)

	try:
		number = int(input("Номер расхода для удаления (0 — отмена): "))
	except ValueError:
		print("Введите целый номер")
		return

	if number == 0:
		return

	if number < 1 or number > len(expenses):
		print("Нет расхода с таким номером")
		return

	deleted = expenses.pop(number - 1)
	save_expenses(expenses)
	print("Удалён расход:", deleted["name"], deleted["amount"])


expenses = load_expenses()

while True:
	print("\n1. Добавить расход")
	print("2. Показать расходы")
	print("3. Удалить расход")
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
		print("Расход добавлен и сохранён:", name, num)

	elif choice == "2":
		show_expenses(expenses)

	elif choice == "3":
		delete_expense(expenses)

	elif choice == "0":
		print("До свидания!")
		break

	else:
		print("Неизвестная команда. Введите 1, 2 или 0.")