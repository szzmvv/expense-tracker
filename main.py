name = input("Введите на что потратились: ")
while True:
	try:
		num = float(input("Введите сумму затраты: "))
	except ValueError:
		print("Введите число, например 150000!")
	else:
		if  num > 0:
			print(name, num )
			break
		else:
			print("Сумма должна быть больше нуля")
