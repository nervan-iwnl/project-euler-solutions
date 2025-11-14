from math import isqrt


per = {}

for a in range(1, 1000):
    for b in range(1, 1000):
        c = isqrt(a * a + b * b)
        if c**2 != a * a + b * b:
            continue
        p = a + b + int(c)
        if p not in per:
            per[p] = set()
        per[p].add((a, b, int(c)))
        
ans = (0, 1)
for k, v in per.items():
    if len(v) > ans[1] and k <= 1000:
        ans = (k, len(v))
    
print(ans[0])