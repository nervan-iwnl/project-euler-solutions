from math import isqrt
from typing import List


def sum_divisors(n: int) -> int:
    if n == 1:
        return 0
    dels = 1
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            dels += d
            q = n // d
            if q != d:
                dels += q
    return dels


abundant_nums = []

for i in range(1, 28124):
    if sum_divisors(i) > i: 
        abundant_nums.append(i)
        
abundant_sum = set()

for i, el in enumerate(abundant_nums):
    for j in abundant_nums[i:]:
        if el + j < 28124:
            abundant_sum.add(el + j)
    
print(sum(n for n in range(1, 28124) if n not in abundant_sum))
