from math import gcd

LIMIT = 160


def unpack_val(v: int) -> int:
    arr = [0] * max(int(3 * v ** (1/3)), 80)
    arr[0] = v

    max_len = 1

    while True:
        shift = 1 if arr[0] <= 1 else 0

        i = 0
        t = 0
        grew = False

        while True:
            t = (t + arr[i + shift]) // 2
            if t == 0:
                break

            if t > arr[i]:
                grew = True

            arr[i] = t
            i += 1

        if not grew:
            break

        max_len = i

    return max_len


def build_G1(limit: int):
    max_c = 3 * limit
    G1 = [0] * (max_c + 1)

    c = 1
    v = 4

    while c <= max_c:
        t = unpack_val(v)

        if t > c:
            G1[c] = v - 1
            c += 1

        v += 4

        if c > max_c:
            break

    return G1


def G(c: int, d: int, G1):
    g = gcd(c, d)
    c //= g
    d //= g

    if d == 1:
        return G1[c]

    idx = 2 * d + c - 3 + (c & 1)

    if c + d <= 5 and d < 4:
        idx -= 1

    return G1[idx]


def solve():
    G1 = build_G1(LIMIT)

    total = 0
    for c in range(1, LIMIT + 1):
        for d in range(1, LIMIT + 1):
            total += G(c, d, G1)

    return total


if __name__ == "__main__":
    print(solve())