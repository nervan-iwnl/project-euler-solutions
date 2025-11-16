def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]


def solve():
    primes = sieve(1_000_000)
    prime_set = set(primes)
    ans = (0, 0)
    prefix_arr = [0]
    for i in primes:
        prefix_arr.append(prefix_arr[-1] + i)
        
    for i in range(len(primes)):
        for j in range(ans[0] + i + 1, len(primes) + 1):
            cum = prefix_arr[j] - prefix_arr[i]
            if cum >= 1_000_000:
                break
            if cum in prime_set:
                ans = (j - i, cum)
        
    return ans

if __name__ == "__main__":
    print(solve())
