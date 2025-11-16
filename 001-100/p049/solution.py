from itertools import permutations


def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]


def solve():
    primes = set(sieve(1000000))
    
    for i in range(1000, 10000):
        for j in permutations(str(i)):
            if i not in primes:
                continue
            j_int = int(''.join(j))
            if j_int != i and j_int in primes:
                k_int = j_int + (j_int - i)
                if k_int in primes and sorted(str(i)) == sorted(str(j_int)) == sorted(str(k_int)) and i != 1487:
                    return str(i) + str(j_int) + str(k_int)
    return None

if __name__ == "__main__":
    print(solve())
