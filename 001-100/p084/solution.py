import random

def next_railway(pos: int) -> int:
    railways = [5, 15, 25, 35]
    for r in railways:
        if r > pos:
            return r
    return 5


def next_utility(pos: int) -> int:
    utilities = [12, 28]
    for u in utilities:
        if u > pos:
            return u
    return 12


def resolve_position(pos: int) -> int:
    while True:
        if pos == 30:
            return 10

        if pos in (2, 17, 33):
            card = random.randint(1, 16)
            if card == 1:
                pos = 0
                continue
            elif card == 2:
                pos = 10
                continue
            else:
                return pos

        if pos in (7, 22, 36):
            card = random.randint(1, 16)

            if card == 1:
                pos = 0
                continue
            elif card == 2:
                pos = 10
                continue
            elif card == 3:
                pos = 11
                continue
            elif card == 4:
                pos = 24
                continue
            elif card == 5:
                pos = 39
                continue
            elif card == 6:
                pos = 5
                continue
            elif card in (7, 8):
                pos = next_railway(pos)
                continue
            elif card == 9:
                pos = next_utility(pos)
                continue
            elif card == 10:
                pos = (pos - 3) % 40
                continue
            else:
                return pos

        return pos


def solve() -> None:
    N = 5_000_000
    cnt = [0] * 40

    pos = 0
    doubles = 0

    for _ in range(N):
        d1 = random.randint(1, 4)
        d2 = random.randint(1, 4)

        if d1 == d2:
            doubles += 1
        else:
            doubles = 0

        if doubles == 3:
            pos = 10
            doubles = 0
        else:
            pos = (pos + d1 + d2) % 40
            pos = resolve_position(pos)

        cnt[pos] += 1

    top3 = sorted(range(40), key=lambda i: -cnt[i])[:3]
    ans = ''.join(f'{x:02d}' for x in top3)
    print(ans)


if __name__ == "__main__":
    solve()