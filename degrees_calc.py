encoder_cpr = 8192

def return_counts(degrees, gear_ratio):
	degrees = int(input("\nEnter degrees of rotation: "))
	counts = (degrees / 360) * (gear_ratio * encoder_cpr)
	return counts

def return_degrees(counts, gear_ratio):
	counts = int(input("\nEnter encoder counts: "))
	degrees = (counts / (gear_ratio * encoder_cpr)) * 360
	return degrees