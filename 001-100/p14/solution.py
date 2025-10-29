from functools import lru_cache

@lru_cache(maxsize=None)
def collatz_len(n: int) -> int:
    if n == 1:
        return 1
    if n % 2 == 0:
        return 1 + collatz_len(n // 2)
    else:
        return 1 + collatz_len(3 * n + 1)


best_n, best_len = 1, 1
for i in range(2, 1_000_001):
    L = collatz_len(i)
    if L > best_len:
        best_len, best_n = L, i


print(best_n) 