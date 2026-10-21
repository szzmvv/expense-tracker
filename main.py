import json


try:
	with open("expenses.json", "r", encoding="utf-8") as file:
		expenses = json.load(file)
except FileNotFoundError:
	expenses = []
while True:
	name = input("На что потратились или 'выход': ")
	if name.strip().lower() == "выход":
		break
	while True:
		try:
			num = float(input("Введите сумму затраты: "))
		except ValueError:
			print("Введите число, например 150000!")
		else:
			if  num > 0:
				print(name, num )
				expenses.append({"name": name, "amount": num})
				break
			else:
				print("Сумма должна быть больше нуля")
total = 0
for expense in expenses:
	print(expense["name"], expense["amount"])
	total = total + expense["amount"]
count = len(expenses)
print("Количество рвсходов: ", count)
print("Всего потрачено: ", total)


with open("expenses.json", "w", encoding="utf-8") as file:
	json.dump(expenses, file, ensure_ascii=False, indent=4)
