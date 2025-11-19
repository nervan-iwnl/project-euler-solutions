def solve():
    ans = 0
    for i in range(1, 1000):
        for power in range(1, 200):
            if len(str(i ** power)) == power:
                ans += 1

    return ans

if __name__ == "__main__":
    print(solve())
