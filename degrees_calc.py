encoder_cpr = 8192

def return_counts(degrees, gear_ratio):
	counts = (degrees / 360) * (gear_ratio * encoder_cpr)
	return int(counts)

def return_degrees(counts, gear_ratio):
	degrees = (counts / (gear_ratio * encoder_cpr)) * 360
	return degrees