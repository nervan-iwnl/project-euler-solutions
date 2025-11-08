ans = 0

for i in range(2, 354295):
    if i == sum(int(digit) ** 5 for digit in str(i)):
        ans += i
        
print(ans)