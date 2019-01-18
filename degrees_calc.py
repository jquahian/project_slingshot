
encoder_cpr = 8192
gear_ratio = int(input("Enter gearing reuduction: "))
counts = int(input("Enter Encoder Counts: "))

degrees = (counts / (gear_ratio * encoder_cpr)) * 360

print("\nEXPECTED ROTATION: {} degrees".format(degrees))