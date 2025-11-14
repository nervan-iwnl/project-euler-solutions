arr = {0: 1, 1: 1, 2: 2, 3: 6, 4: 24, 5: 120, 6: 720, 7: 5040, 8: 40320, 9: 362880}

ans = 0

def digitsum(n):
    s = 0
    while n > 0:
        s += arr[n % 10]
        n //= 10
    return s

for i in range(3, 10**7 + 1):
    if i == digitsum(i):
        ans += i
        
print(ans)