from math import isqrt


def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]


def solve():
    primes = set((sieve(100000)))
    ans = -1
    
    for i in range(3, 1000000, 2):
        if i in primes:
            continue
        was_found = False
        for j in range(1, isqrt(i) + 1):
            if i - j * j * 2 in primes:
                was_found = True
                
        if not was_found:
            return i
    
    return None

if __name__ == "__main__":
    print(solve())
