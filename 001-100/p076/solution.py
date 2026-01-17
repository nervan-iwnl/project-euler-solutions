def solve():
    n = 100
    dp = [0] * (n + 1)
    dp[0] = 1
    for k in range(1, n):
        for s in range(k, n + 1):
            dp[s] += dp[s - k]
    return dp[n]

 
if __name__ == "__main__":
    print(solve())
