from math import isqrt
from typing import List


def find_divisors(n: int) -> List[int]:
    n = abs(n)
    small, large = 0, 0
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            small += 1
            q = n // d
            if q != d:
                large += 1
    return small + large

    
    

num = 1
for i in range(2, 1_000_000):
    num += i
    if find_divisors(num) >= 500:
        print(num)
        exit()