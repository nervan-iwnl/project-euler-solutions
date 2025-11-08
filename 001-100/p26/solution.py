def cycle_len(d: int) -> int:
    n = d
    seen = {}               
    r = 1 % n
    pos = 0
    while r not in seen:
        seen[r] = pos
        r = (r * 10) % n
        pos += 1
    return pos - seen[r]    


max_cycle = 0
max_i = 0
for i in range(1, 1000):
    if cycle_len(i) > max_cycle:
        max_cycle = cycle_len(i)
        max_i = i
print(max_i)