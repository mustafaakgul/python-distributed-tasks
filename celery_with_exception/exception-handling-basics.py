class SalaryError(Exception):
	pass


while True:
	try:
		salary = input("Please enter your salary")
		if not salary.isdigit():
			raise SalaryError()
		print(salary)
		break
	except SalaryError:
		print("invalid salary amount, please try again...")
	finally:
		print("this will get executed no matter what")
