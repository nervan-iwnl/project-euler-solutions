from math import sqrt

def is_pandigital(n):
    for i in range(1, int(sqrt(n)) + 1):
        if n % i == 0:
            if i != n // i:
                if sorted(str(i) + str(n // i) + str(n)) == ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return True
                                  
    return False




ans = 0
for i in range(100, 10000):
    if is_pandigital(i):
        ans += i
        
print(ans)