from typing import List
from math import isqrt

def sieve(n: int) -> List[int]:
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    limit = int(n ** 0.5)
    for p in range(2, limit + 1):
        if is_prime[p]:
            start = p * p
            step = p
            is_prime[start:n + 1:step] = [False] * (((n - start) // step) + 1)

    return [i for i, ok in enumerate(is_prime) if ok]


def solve():
    ans = (-1, -1)
    primes = sieve(1_000_000)
    for i in range(1, 1_000_001):
        curr = 1
        for j in range(0, isqrt(i) + 1):
            if i % primes[j] == 0:
                curr *= (1/(1 - 1/primes[j]))
            if primes[j] >= isqrt(i) + 1:
                break
        if curr > ans[0]:
            ans = (curr, i)
    
    return ans[1]


if __name__ == "__main__":
    print(solve())
 