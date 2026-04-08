def solve():
    K = 12_000
    lim = 2 * K
    best = [10 ** 9] * (K + 1)
    def dfs(prod, sum_, count, start):
        k = count + (prod - sum_)
        if k <= K:
            if prod < best[k]:
                best[k] = prod
        else:
            return  
        
        for f in range(start, lim // prod + 1):
            new_prod = prod * f 
            new_sum = f + sum_ 
            if new_prod > lim:
                break
            dfs(new_prod, new_sum, count + 1, f)
    
    dfs(1, 0, 0, 2)
    return sum(set(best[2:]))


if __name__ == "__main__":
    print(solve())
