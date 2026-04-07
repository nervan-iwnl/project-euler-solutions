def solve():
    N = 1_000_000
    sum_div = [0] * (N + 1)

    for i in range(1, N // 2 + 1):
        for j in range(2 * i, N + 1, i):
            sum_div[j] += i

    ans = (0, 0)
    visited = set()

    for i in range(1, N + 1):
        if i in visited:
            continue

        curr = i
        path = []
        pos = {}

        while 1 <= curr <= N and curr not in visited and curr not in pos:
            pos[curr] = len(path)
            path.append(curr)
            curr = sum_div[curr]

        if 1 <= curr <= N and curr in pos:
            cycle = path[pos[curr]:]
            if len(cycle) > ans[0]:
                ans = (len(cycle), min(cycle))
            elif len(cycle) == ans[0]:
                ans = (ans[0], min(ans[1], min(cycle)))

        visited.update(path)

    return ans[1]

if __name__ == "__main__":
    print(solve())