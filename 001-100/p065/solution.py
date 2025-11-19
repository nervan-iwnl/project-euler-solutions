from fractions import Fraction

def solve():
    arr = [2, 1] + [x for i in range(1, 100) for x in (2 * i, 1, 1)]
    
    frac = Fraction(arr[99], 1)
    for i in range(98, -1, -1):
        frac = arr[i] + 1/frac
        
    return sum(int(i) for i in str(frac.numerator))

if __name__ == "__main__":
    print(solve())
