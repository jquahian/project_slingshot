# 100,000 counts = ~35 - 40 degrees

encoder_cpr = 8192
gear_ratio = 64
counts = 200000

degrees = (counts / (gear_ratio * encoder_cpr)) * 360

print(degrees)