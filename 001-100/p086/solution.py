from math import isqrt

def solve():
    cnt = 0
    N = 1_000_000
    for c in range(1, N):
        for s in range(2, 2 * c + 1):
            x = c ** 2 + s ** 2
            if isqrt(x)**2 != x:
                continue
            if s <= c:
                cnt += s // 2
            else:
                cnt += s // 2 - (s - c) + 1
            if cnt > N:
                return c
    return None

if __name__ == "__main__":
    print(solve())
