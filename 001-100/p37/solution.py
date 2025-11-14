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


is_prime = sieve(2_000_000)

ans = 0

for i in range(10, 2_000_000):
    if all(is_prime[int(str(i)[j:])] for j in range(len(str(i)))):
        rev = all(is_prime[int(str(i)[:len(str(i))-j])] for j in range(len(str(i))))
        if rev:
            ans += i
            
print(ans)