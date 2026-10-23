import math
import sqlite3


def read_amount():
	while True:
		try:
			amount = float(input("Введите сумму затраты: "))
		except ValueError:
			print("Введите число, например 150000!")
			continue

		if math.isfinite(amount) and amount > 0:
			return amount

		print("Сумма должна быть положительным конечным числом")


def init_db():
	connection = sqlite3.connect("expenses.db")

	try:
		connection.execute("""
			CREATE TABLE IF NOT EXISTS expenses (
				id INTEGER PRIMARY KEY,
				name TEXT NOT NULL,
				amount REAL NOT NULL CHECK(amount > 0),
				category TEXT NOT NULL
			)
		""")
		connection.commit()
	finally:
		connection.close()


def add_expense_db(name, amount, category):
	connection = sqlite3.connect("expenses.db")

	try:
		connection.execute(
			"INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)",
			(name, amount, category)
		)
		connection.commit()
	finally:
		connection.close()


def load_expenses_db():
	connection = sqlite3.connect("expenses.db")
	connection.row_factory = sqlite3.Row

	try:
		rows = connection.execute(
			"SELECT id, name, amount, category FROM expenses ORDER BY id"
		).fetchall()

		return [dict(row) for row in rows]
	finally:
		connection.close()


def delete_expense_db(expense_id):
	connection = sqlite3.connect("expenses.db")

	try:
		cursor = connection.execute(
			"DELETE FROM expenses WHERE id = ?",
			(expense_id,)
		)
		connection.commit()
		return cursor.rowcount
	finally:
		connection.close()


def show_expenses(expenses):
	if not expenses:
		print("Расходов пока нет.")
		return

	total = 0

	for number, expense in enumerate(expenses, start=1):
		print(
			number,
			expense["name"],
			expense["amount"],
			"Категория:",
			expense["category"]
		)
		total = total + expense["amount"]

	print("Количество расходов:", len(expenses))
	print("Всего потрачено:", total)


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

	expense = expenses[number - 1]
	deleted_count = delete_expense_db(expense["id"])

	if deleted_count == 1:
		print("Удалён расход:", expense["name"], expense["amount"])
	else:
		print("Запись не найдена")


def show_category_total(expenses):
	category = input("Введите категорию: ").strip().lower()

	if not category:
		print("Категория не должна быть пустой")
		return

	total = 0
	count = 0

	for expense in expenses:
		if expense["category"].strip().lower() == category:
			total = total + expense["amount"]
			count = count + 1

	print("Найдено расходов:", count)
	print("Сумма по категории:", total)


def main():
	init_db()

	while True:
		print("\n1. Добавить расход")
		print("2. Показать расходы")
		print("3. Удалить расход")
		print("4. Показать сумму по категории")
		print("0. Выйти")

		choice = input("Выберите действие: ").strip()

		if choice == "1":
			name = input("На что потратились: ").strip()

			if not name:
				print("Название не должно быть пустым")
				continue

			category = input("Категория: ").strip()

			if not category:
				print("Категория не должна быть пустой")
				continue

			amount = read_amount()
			add_expense_db(name, amount, category)
			print("Расход добавлен и сохранён:", name, amount)

		elif choice == "2":
			show_expenses(load_expenses_db())

		elif choice == "3":
			delete_expense(load_expenses_db())

		elif choice == "4":
			show_category_total(load_expenses_db())

		elif choice == "0":
			print("До свидания!")
			break

		else:
			print("Неизвестная команда. Введите 1, 2, 3, 4 или 0.")


if __name__ == "__main__":
	main()