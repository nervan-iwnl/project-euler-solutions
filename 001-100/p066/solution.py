from math import isqrt


def x_D(D: int) -> int | None:
    a0 = isqrt(D)
    if a0 * a0 == D:
        return None 

    m, d, a = 0, 1, a0
    
    p_prev, p = 1, a0
    q_prev, q = 0, 1
    while True:
        m = d * a - m
        d = (D - m * m) // d
        a = (a0 + m) // d   
        
        p_prev, p = p, a * p + p_prev
        q_prev, q = q, a * q + q_prev

        if p**2 - D * q * q == 1:
            return p



def solve():
    ans = (-1, -1)
    for d in range(2, 1001):
        res = x_D(d)
        if res and ans[0] < res:
            ans = (res, d)
    return ans[1]

if __name__ == "__main__":
    print(solve())
