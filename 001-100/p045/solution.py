def solve():
    pentagonal_numbers = [i * (i * 3 - 1) // 2 for i in range(1, 60000)]
    pentagonal_set = set(pentagonal_numbers)
    
    triangular_numbers = [i * (i + 1) // 2 for i in range(1, 60000)]
    triangular_set = set(triangular_numbers)
    
    hexoganal_numbers = [i * (2 * i - 1) for i in range(1, 60000)]
    
    for i in hexoganal_numbers:
        if (i in pentagonal_set and i in triangular_set) and (i != 1 and i != 40755):
            return i
    
    return None

if __name__ == "__main__":
    print(solve())
