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
    LIM = 50_000_000
    ans = set()
    sq = sieve(isqrt(LIM) + 1)
    cube = sieve(int((LIM) ** (1/3)) + 1)
    bi_sq = sieve(int((LIM) ** (1/4)) + 1) 
    for i in sq:
        for j in cube:
            for k in bi_sq:
                tmp = i**2 + j**3 + k**4
                if tmp >= LIM:
                    continue
                ans.add(tmp)
    return len(ans)


if __name__ == "__main__":
    print(solve())
