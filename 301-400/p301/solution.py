def solve():
    f = [0] * 32
    f[0] = 1
    f[1] = 2

    for i in range(2, 31):
        f[i] = f[i-1] + f[i-2]

    return f[30]


print(solve())