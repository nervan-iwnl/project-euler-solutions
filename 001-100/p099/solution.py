from math import log10

def solve():
    ans = (0, 0)
    with open('base_exp.txt') as f:
        for i, line in enumerate(f.readlines()):
            base, exp = [int(_) for _ in line.split(',')]
            curr = exp * log10(base)
            if (curr > ans[0]):
                ans = (curr, i)
    return ans[1] + 1
                

if __name__ == "__main__":
    print(solve())
