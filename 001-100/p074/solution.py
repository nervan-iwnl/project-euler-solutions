fac = [1]
for i in range(1, 10):
    fac.append(fac[-1] * i)
    
seen = [-1] * 2540161

for i in range(len(seen)):
    if seen[i] != -1:
        continue
    chain = []
    n = i
    while seen[n] == -1 and n not in chain:
        chain.append(n)
        s = [fac[int(c)] for c in str(n)]
        n = sum(s)
        
    if n in chain:
        loop_start = chain.index(n)
        cycle_len = len(chain) - loop_start
        for j in range(loop_start, len(chain)):
            seen[chain[j]] = cycle_len
        for j in range(loop_start - 1, -1, -1):
            seen[chain[j]] = seen[chain[j + 1]] + 1
    else:
        base = seen[n]
        for j in range(len(chain) - 1, -1, -1):
            base += 1
            seen[chain[j]] = base
            
            
print(sum(1 for i in range(1000000) if seen[i] == 60))