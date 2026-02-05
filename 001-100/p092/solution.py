def solve():
    MAX_N = 10_000_000

    if_89 = {89}
    seen = [False] * (MAX_N + 1)

    for n in range(1, MAX_N):
        if n <= MAX_N and seen[n]:
            continue

        chain = [] 
        current = n

        while current != 1 and current != 89 and current not in if_89:
            chain.append(current)
            next_num = sum(int(digit) ** 2 for digit in str(current))
            current = next_num

        if current == 89 or current in if_89:
            for x in chain:
                if x <= MAX_N:
                    if_89.add(x)
                    seen[x] = True
        else:
            for x in chain:
                if x <= MAX_N:
                    seen[x] = True

    return if_89


if __name__ == "__main__":
    res = solve()
    print(len(res))  
