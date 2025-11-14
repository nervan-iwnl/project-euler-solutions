def is_pallinrome(string : str) -> bool:
    return string == string[::-1]



ans = 0

for i in range(1, 1_000_000):
    if is_pallinrome(str(i)) and is_pallinrome(bin(i)[2:]):
        ans += i

print(ans)