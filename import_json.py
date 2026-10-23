import json
import math
import sqlite3
from pathlib import Path

from main import init_db


folder = Path(__file__).resolve().parent
json_path = folder / "expenses.json"
db_path = folder / "expenses.db"

with json_path.open("r", encoding="utf-8") as file:
	expenses = json.load(file)

if not isinstance(expenses, list):
	raise SystemExit("JSON должен содержать список расходов")

records = []

for number, expense in enumerate(expenses, start=1):
	if not isinstance(expense, dict):
		raise SystemExit(f"Запись {number}: ожидался словарь")

	name = expense.get("name")
	amount = expense.get("amount")
	category = expense.get("category", "Без категории")

	if not isinstance(name, str) or not name.strip():
		raise SystemExit(f"Запись {number}: неверное название")

	if not isinstance(category, str) or not category.strip():
		raise SystemExit(f"Запись {number}: неверная категория")

	if (
		type(amount) not in (int, float)
		or not math.isfinite(amount)
		or amount <= 0
	):
		raise SystemExit(f"Запись {number}: неверная сумма")

	records.append((name.strip(), amount, category.strip()))

# main.py пока использует путь относительно текущей папки.
# Запускайте скрипт из папки проекта.
if Path.cwd().resolve() != folder:
	raise SystemExit("Запустите скрипт из папки проекта")

init_db()
connection = sqlite3.connect(db_path)

try:
	with connection:
		connection.execute("""
			CREATE TABLE IF NOT EXISTS imports (
				source TEXT PRIMARY KEY
			)
		""")

		cursor = connection.execute(
			"INSERT OR IGNORE INTO imports (source) VALUES (?)",
			("expenses.json-v1",)
		)

		if cursor.rowcount == 0:
			print("Этот JSON уже импортирован. Повторного добавления нет.")
		else:
			connection.executemany(
				"""
				INSERT INTO expenses (name, amount, category)
				VALUES (?, ?, ?)
				""",
				records
			)
			print("Добавлено расходов:", len(records))
finally:
	connection.close()