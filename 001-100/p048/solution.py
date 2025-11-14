def solve():
    MOD = 10**10
    ans = 0
    for i in range(1, 1001):
        ans = (ans + (i ** i)) % (10**10)
    return ans

if __name__ == "__main__":
    print(solve())
