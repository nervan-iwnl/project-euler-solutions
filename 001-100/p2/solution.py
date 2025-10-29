arr = [1, 2]

while arr[-1] <= 4_000_000: 
    arr.append(arr[-1] + arr[-2])


ans = 0    
for i, el in enumerate(arr): 
    if el % 2 == 0: 
        ans += el

print(ans)
print(arr)