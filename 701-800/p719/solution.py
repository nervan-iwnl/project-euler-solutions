def is_s_number(k: int) -> bool:
    n = k * k
    s = str(n)
    L = len(s)
    target = k

    digits = [int(ch) for ch in s]

    min_tail = [0] * (L + 1)
    for i in range(L - 1, -1, -1):
        min_tail[i] = min_tail[i + 1] + digits[i]

    max_tail = [0] * (L + 1)
    power10 = 1
    for i in range(L - 1, -1, -1):
        max_tail[i] = digits[i] * power10 + max_tail[i + 1]
        power10 *= 10

    if min_tail[0] > target or max_tail[0] < target:
        return False

    def dfs(pos: int, cur_sum: int, parts: int) -> bool:
        if cur_sum > target:
            return False

        if pos == L:
            return cur_sum == target and parts >= 2

        if cur_sum + min_tail[pos] > target:
            return False
        if cur_sum + max_tail[pos] < target:
            return False

        val = 0
        for end in range(pos, L):
            if end > pos and digits[pos] == 0:
                break

            val = val * 10 + digits[end]

            if cur_sum + val > target:
                break

            if dfs(end + 1, cur_sum + val, parts + 1):
                return True

        return False

    return dfs(0, 0, 0)



def solve():
    prev = -1
    ans = 0
    for i in range(1, 10**6 + 1):
        if i // 10000 != prev:
            prev = i // 10000
            print(prev)
            
        if is_s_number(i):
            ans += i**2
    return ans

if __name__ == "__main__":
    print(solve())
