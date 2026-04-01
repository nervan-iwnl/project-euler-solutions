from math import sqrt, isqrt

def solve():
    ans = 0
    lim = 1_000_000_000
    x, y = 2, 1
    while True:
        x, y = 2 * x + 3 * y, x + 2 * y
        
        if (2 * x - 1) % 3 == 0:
            a = (2 * x - 1) // 3
            p = 3 * a - 1
            if p <= lim:
                ans += p
        if (2 * x + 1) % 3 == 0:
            a = (2 * x + 1) // 3
            p = 3 * a + 1 
            if p <= lim:
                ans += p
        if p > lim:
            break
    return ans

if __name__ == "__main__":
    print(solve())
