a, b = 1, 1

idx = 2
while len(str(b)) < 1000:
    a, b = b, a + b
    idx += 1

print(idx)

