from itertools import permutations


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
    arr = '123456789'
    
    while len(arr) > 1:
        for i in permutations(arr[::-1]):
            if is_prime(int(''.join(i))):
                return int(''.join(i))
        arr = arr[:-1]
    return None

if __name__ == "__main__":
    print(solve())
