from math import isqrt


def next_step(a, m, d, N):
    m1 = d * a - m
    d1 = (N - m1**2) // d
    a1 = (isqrt(N) + m1) // d1
    return a1, m1, d1, N        


def solve():
    ans = 0
    for i in range(1, 10_001):
        num = i 
        dict_params = {}
        a, m, d, N = isqrt(num), 0, 1, num
        if a ** 2 == num:
            continue
        dict_params[(a, m, d)] = 0
        idx = 0
        while True:
            a, m, d, N = next_step(a, m, d, N)
            key = (a, m, d)
            idx += 1
            if key in dict_params:
                if (idx - dict_params[key]) % 2 == 1:
                    ans += 1
                break
            else: 
                dict_params[key] = idx 
    return ans

if __name__ == "__main__":
    print(solve())
