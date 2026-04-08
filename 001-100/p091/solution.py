from math import gcd

def solve():
    N = 50
    ans = 3 * N * N

    for x in range(1, N + 1):
        for y in range(1, N + 1):
            g = gcd(x, y)
            dx = y // g
            dy = x // g
            ans += 2 * min(x // dx, (N - y) // dy)

    return ans


if __name__ == "__main__":
    print(solve())