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


try:
	with open("expenses.json", "r", encoding="utf-8") as file:
		expenses = json.load(file)
except FileNotFoundError:
	expenses = []

while True:
	name = input("На что потратились или 'выход': ")

	if name.strip().lower() == "выход":
		break

	if not name.strip():
		print("Название не должно быть пустым")
		continue

	num = read_amount()
	print(name, num)
	expenses.append({"name": name, "amount": num})

total = 0

for expense in expenses:
	print(expense["name"], expense["amount"])
	total = total + expense["amount"]

count = len(expenses)
print("Количество расходов:", count)
print("Всего потрачено:", total)

with open("expenses.json", "w", encoding="utf-8") as file:
	json.dump(expenses, file, ensure_ascii=False, indent=4)