from math import gcd

def solve():
    ans = 0
    for d in range(1, 12_000 + 1):
        n_min = d // 3
        n_max = (d + 1) // 2
        for n in range(n_min + 1, n_max):
            if gcd(n, d) == 1:
                ans += 1

    return ans

if __name__ == "__main__":
    print(solve())
