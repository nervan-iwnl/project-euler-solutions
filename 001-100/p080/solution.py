from decimal import Decimal, getcontext
import math

getcontext().prec = 110
ans = 0

for i in range(1, 101):
    if int(math.isqrt(i))**2 == i:
        continue
    
    x = str(Decimal(i).sqrt()).replace('.', '')[:100]
    ans += sum(map(int, x))

print(ans)