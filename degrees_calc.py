encoder_cpr = 8192
gear_ratio = int(input("Enter gearing reuduction: "))

def menu():
	choice = input("\n(a) return counts \n(b) return degrees \n(c) quit \n\n")

	if choice.lower() == "a":
		return_counts()
	elif choice.lower() =="b":
		return_degrees()
	else:
		quit()

def return_counts():
	degrees = int(input("\nEnter degrees of rotation: "))
	counts = (degrees / 360) * (gear_ratio * encoder_cpr)
	print("\nENCODER COUNTS: {} to rotate {} degrees".format(counts, degrees))
	menu()

def return_degrees():
	counts = int(input("\nEnter encoder counts: "))
	degrees = (counts / (gear_ratio * encoder_cpr)) * 360
	print("\nROTATION OF: {} degrees with {} encoder counts".format(degrees, counts))
	menu()

menu()