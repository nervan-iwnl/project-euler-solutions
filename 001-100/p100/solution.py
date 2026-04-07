def solve():
    x, y = 1, 1
    while True:
        n, b = (x + 1) // 2, (y + 1) // 2
        if n >= 10**12:
            return b
        x, y = 3 * x + 4 * y, 2 * x + 3 * y
        
        
if __name__ == "__main__":
    print(solve())
