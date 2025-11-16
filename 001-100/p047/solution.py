from math import isqrt


def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]


def find_dels(n, primes_set):
    dels = []
    for i in range(1, isqrt(n) + 1):
        if n % i == 0 and (i in primes_set or n // i in primes_set):
            if i in primes_set:
                dels.append(i)
            if i != n // i and n // i in primes_set:
                dels.append(n // i)
    return dels


def solve():
    primes = set((sieve(100000)))
    
    curr_seq = 0
    for i in range(3, 1000000):
        if len(find_dels(i, primes)) >= 4:
            curr_seq += 1
            if curr_seq == 4:
                return i - 3
        else:
            curr_seq = 0
        
    return None

if __name__ == "__main__":
    print(solve())
