def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def solve():
    prime_cnt = 0
    for i in range(3, 100_000, 2):
        corners = [(i - 2) ** 2 + (i - 1) * k for k in range(1, 5)]
        prime_cnt += sum(is_prime(j) for j in corners)
        if prime_cnt / (i * 2 - 1) < 0.1:
            return i
    
    return None

if __name__ == "__main__":
    print(solve())
