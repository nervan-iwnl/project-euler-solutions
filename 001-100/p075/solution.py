from math import gcd, isqrt


def solve():
    lim = 15 * 10**5
    M = isqrt(lim // 2) + 1
    dic = {}
    for m in range(2, M + 1):
        for n in range(1, m):
            if gcd(m, n) == 1 and (m + n) % 2 == 1:
                sum_len = 2 * m * (m + n)
                for k in range(sum_len, lim + 1, sum_len):
                    dic[k] = dic.get(k, 0) + 1
    return sum(1 for v in dic.values() if v == 1)


if __name__ == "__main__":
    print(solve())
