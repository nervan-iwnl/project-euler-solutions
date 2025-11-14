def spiral_diag_sum(n: int) -> int:
    total = 1
    for k in range(1, (n - 1) // 2 + 1):
        total += 4 * (2 * k + 1) ** 2 - 12 * k
    return total


print(spiral_diag_sum(1001))