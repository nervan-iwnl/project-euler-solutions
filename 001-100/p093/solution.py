from itertools import combinations, permutations, product
from fractions import Fraction


def apply_op(x, y, op):
    if op == '+':
        return x + y
    if op == '-':
        return x - y
    if op == '*':
        return x * y
    if op == '/':
        if y == 0:
            return None
        return x / y


def all_results(a, b, c, d, op1, op2, op3):
    res = []

    # ((a op b) op c) op d
    x = apply_op(a, b, op1)
    if x is not None:
        y = apply_op(x, c, op2)
        if y is not None:
            z = apply_op(y, d, op3)
            if z is not None:
                res.append(z)

    # (a op (b op c)) op d
    x = apply_op(b, c, op2)
    if x is not None:
        y = apply_op(a, x, op1)
        if y is not None:
            z = apply_op(y, d, op3)
            if z is not None:
                res.append(z)

    # a op ((b op c) op d)
    x = apply_op(b, c, op2)
    if x is not None:
        y = apply_op(x, d, op3)
        if y is not None:
            z = apply_op(a, y, op1)
            if z is not None:
                res.append(z)

    # a op (b op (c op d))
    x = apply_op(c, d, op3)
    if x is not None:
        y = apply_op(b, x, op2)
        if y is not None:
            z = apply_op(a, y, op1)
            if z is not None:
                res.append(z)

    # (a op b) op (c op d)
    x = apply_op(a, b, op1)
    y = apply_op(c, d, op3)
    if x is not None and y is not None:
        z = apply_op(x, y, op2)
        if z is not None:
            res.append(z)

    return res


def consecutive_length(values):
    n = 1
    while n in values:
        n += 1
    return n - 1


def solve():
    ops = ['+', '-', '*', '/']
    best_len = 0
    best_digits = None

    for digits in combinations(range(1, 10), 4):
        values = set()

        for p in permutations(digits):
            a, b, c, d = map(Fraction, p)

            for op1, op2, op3 in product(ops, repeat=3):
                for val in all_results(a, b, c, d, op1, op2, op3):
                    if val.denominator == 1 and val > 0:
                        values.add(val.numerator)

        curr_len = consecutive_length(values)
        if curr_len > best_len:
            best_len = curr_len
            best_digits = digits

    return ''.join(map(str, best_digits))


if __name__ == "__main__":
    print(solve())