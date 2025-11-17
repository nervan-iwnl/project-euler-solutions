from math import comb 

def solve():
    ans = 0
    for n in range(1, 101):
        for r in range(0, n + 1):
            if comb(n, r) >= 1_000_000:
                ans += 1
    return ans

if __name__ == "__main__":
    print(solve())
