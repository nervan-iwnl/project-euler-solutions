from functools import lru_cache

@lru_cache(maxsize=None)
def next_step(num: int, step: int):
    if step == 50:
        return False
    
    num += int(str(num)[::-1])
    if str(num) == str(num)[::-1]:
        return True
    
    return next_step(num, step + 1)


def solve():
    ans = 0
    for i in range(1, 10_001):
        if not next_step(i, 0):
            ans += 1
    return ans 


if __name__ == "__main__":
    print(solve())
