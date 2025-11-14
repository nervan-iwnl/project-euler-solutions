num = 600851475143
dels = []
i = 2

while num > 1: 
    if num % i == 0:
        dels.append(i)
        num //= i 
    i += 1
    

print(dels[-1])