def sieve(n: int):
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
    n = 200
    dp = [0] * (n + 1)
    dp[0] = 1
    prime = sieve(n)
    for k in prime:
        for s in range(k, n + 1):
            dp[s] += dp[s - k]
    return [i for i, v in enumerate(dp) if v > 5000][0]

 
if __name__ == "__main__":
    print(solve())

