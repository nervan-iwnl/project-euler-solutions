def solve():
    pentagonal_numbers = [i * (i * 3 - 1) // 2 for i in range(1, 5000)]
    pentagonal_set = set(pentagonal_numbers)
    
    ans = (-1, -1)
    
    for i in range(len(pentagonal_numbers)):
        for j in range(i + 1, len(pentagonal_numbers)):
            Pj = pentagonal_numbers[j]
            Pi = pentagonal_numbers[i]
            if (Pj - Pi in pentagonal_set and Pj + Pi in pentagonal_set) and (Pj - Pi < ans[0] or ans[0] == -1):
                ans = (Pj - Pi, Pj + Pi)
    return ans
    
if __name__ == "__main__":
    print(solve())
