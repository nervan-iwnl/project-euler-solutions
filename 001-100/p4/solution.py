def is_polly(num):
    if len(str(num)) % 2 == 0:
        return str(num)[0:len(str(num)) // 2] == str(num)[len(str(num)):len(str(num)) // 2 - 1: -1]
    else:
        return str(num)[0:len(str(num)) // 2] == str(num)[len(str(num)):len(str(num)) // 2: -1]
    

max_polly = -1
for i in range(100, 1000):
    for j in range(100, 1000):
        if is_polly(i * j):
            max_polly = max(i * j, max_polly)
            
print(max_polly)