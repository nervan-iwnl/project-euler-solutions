from itertools import permutations


def is_feature(n: int) -> bool:
    n = str(n)
    if int(n[1:4]) % 2 != 0:
        return False
    if int(n[2:5]) % 3 != 0:
        return False
    if int(n[3:6]) % 5 != 0:
        return False
    if int(n[4:7]) % 7 != 0:
        return False
    if int(n[5:8]) % 11 != 0:
        return False
    if int(n[6:9]) % 13 != 0:
        return False
    if int(n[7:10]) % 17 != 0:
        return False
    return True
    

def solve():
    arr = '0123456789'
    ans = 0
    for i in permutations(arr[::-1]):
        if i[0] == '0':
            continue
        if is_feature(int(''.join(i))):
            ans += int(''.join(i))
    return ans


if __name__ == "__main__":
    print(solve())
