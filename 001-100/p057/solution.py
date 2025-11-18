from fractions import Fraction

def solve():
    ans = 0
    frac = 1 + Fraction('1/2')
    for i in range(1000):
        frac = 1 + (1 / (2 + frac - 1))
        if len(str(frac.numerator)) > len(str(frac.denominator)):
            ans += 1 
    return ans

if __name__ == "__main__":
    print(solve())
