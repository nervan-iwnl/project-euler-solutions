from typing import List

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

    return {i for i, ok in enumerate(is_prime) if ok}



prime_set = sieve(2_000_000)

max_n = 0
max_a = 0
max_b = 0
for a in range(-999, 1000):
    for b in range(-1000, 1001):
        n = 0
        while True:
            val = n * n + a * n + b
            if val in prime_set:
                n += 1
            else:
                break
        if n > max_n:
            max_n = n
            max_a = a
            max_b = b
            
print(max_a * max_b)