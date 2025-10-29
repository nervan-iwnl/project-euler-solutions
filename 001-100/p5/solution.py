import math

ans = 1
for x in range(2, 21):
    ans = ans * x // math.gcd(ans, x)

print(ans)
