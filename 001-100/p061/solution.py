def P3(n): return n*(n+1)//2
def P4(n): return n*n
def P5(n): return n*(3*n-1)//2 
def P6(n): return n*(2*n-1)
def P7(n): return n*(5*n-3)//2
def P8(n): return n*(3*n-2)

polys = {k: [] for k in range(3, 9)}
by_prefix = {k: {} for k in range(3, 9)}


def dfs(path, types_used):
    if len(path) == 6:
        if path[0] // 100 == path[-1] % 100:
            return sum(path) 
        return None
    
    if not path:
        for t in [3, 4, 5, 6, 7, 8]:
            for x in polys[t]:
                pref = x // 100 
                suf = x % 100
                if suf < 10:
                    continue
                res = dfs([x], {t})
                if res:
                    return res
        return None
                
    else:
        tail = path[-1] % 100
        for t in {3, 4, 5, 6, 7, 8}.difference(types_used):
            for x in by_prefix[t].get(tail, []):
                res = dfs(path + [x], types_used | {t})
                if res:
                    return res
        return None

def solve():
    for k, f in [(3, P3), (4, P4), (5, P5), (6, P6), (7, P7), (8, P8)]:
        n = 1
        while True:
            x = f(n)
            if x > 9999:
                break
            if 1000 <= x <= 9999:
                polys[k].append(x)
            n += 1
    for k in range(3, 9):
        for x in polys[k]:
            pref = x // 100
            suf = x % 100
            if suf < 10:
                continue
            by_prefix[k].setdefault(pref, []).append(x) 

    return dfs([], set())

if __name__ == "__main__":
    print(solve())
