import math

def solve():
    ans = (0, 0, 0)
    target = 2_000_000
    for m in range(1, 1_000_001):
        a = (m + 1) * m // 2
        x = 2 * target / a
        n = int((-1 + math.sqrt(1 + 4 * x)) / 2)
        curr = (n * (n + 1) // 2) * (m * (m + 1) // 2)
        if ans[0] < curr <= target:
            ans = (curr, m, n)
    
    return ans[1] * ans[2]

if __name__ == "__main__":
    print(solve())
