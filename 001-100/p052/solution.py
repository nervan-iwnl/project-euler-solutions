def solve():
    for i in range(1, 1_000_000):
        if sorted(str(i)) == sorted(str(i * 2)) == sorted(str(i * 3)) == sorted(str(i * 4)) == sorted(str(i * 5)) == sorted(str(i * 6)):
            return i
    return None

if __name__ == "__main__":
    print(solve())
