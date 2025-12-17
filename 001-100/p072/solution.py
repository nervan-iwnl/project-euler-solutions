def solve():
    ans = 0
    N = 1_000_000
    phi = list(range(N + 1))

    for p in range(2, N + 1):
        if phi[p] == p:           
            for k in range(p, N + 1, p):
                phi[k] -= phi[k] // p

    return sum(phi[2:N + 1])


if __name__ == "__main__":
    print(solve())
