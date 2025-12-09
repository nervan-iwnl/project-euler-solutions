def solve():
    N = 10_000_000
    phi = list(range(N + 1))

    for p in range(2, N + 1):
        if phi[p] == p:           
            for k in range(p, N + 1, p):
                phi[k] -= phi[k] // p

    ans = (10**11, -1)
    for i in range(2, N + 1):
        if sorted(str(i)) == sorted(str(phi[i])):
            ratio = i / phi[i]
            if ratio < ans[0]:
                ans = (ratio, i)
    return ans[1]


if __name__ == "__main__":
    print(solve())
