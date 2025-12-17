from math import gcd

def solve():
    ans = (0, 1)
    for d in range(1, 10**6 + 1):
        n = (d * 3 - 1) // 7
        if n != 0 and d * ans[0] < n * ans[1]:
            if gcd(n, d) == 1:
                ans = (n, d)
            
    return ans[0]
    
    
if __name__ == "__main__":
    print(solve())
