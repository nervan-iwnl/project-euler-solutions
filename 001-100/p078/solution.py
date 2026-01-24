def solve(): 
    p = [0, 1] 
    while p[-1] % 10**6 != 0: 
        n = len(p) 
        new = 0 
        q = 1 
        while n - (3 * q**2 - q) // 2 >= 0:
            new += (-1) **(q + 1) * (p[max(0, n - (3 * q**2 - q) // 2)] + p[max(0, n - (3 * q**2 + q) // 2)]) 
            q += 1 
        p.append(new % 10**6) 
    return len(p) - 2 


if __name__ == "__main__": 
    print(solve())