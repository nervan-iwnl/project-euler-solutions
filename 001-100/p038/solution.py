ans = 0

for i in range(1, 1000000):
    curr_str = str(i)
    mul = 2
    while len(curr_str) < 9:
        curr_str += str(i * mul)
        mul += 1
    if len(curr_str) == 9 and set(curr_str) == set("123456789"):
        ans = max(ans, int(curr_str))
        
print(ans)