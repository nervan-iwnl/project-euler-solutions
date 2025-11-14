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

    return is_prime


is_prime = sieve(1_000_000 - 1)
ans = 0

for i in range(2, 1_000_000):
    s = str(i)
    if all(is_prime[int(s[j:] + s[:j])] for j in range(len(s))):
        ans += 1
        pass
    else:
        is_prime[i] = False
        
print(ans)