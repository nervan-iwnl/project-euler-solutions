def solve():
    ans = 0
    for a in range(1, 100):
        for b in range(1, 100):
            ans = max(ans, sum(map(int, str(abs(a ** b)))))

    return ans

if __name__ == "__main__":
    print(solve())
