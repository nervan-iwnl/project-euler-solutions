from math import isqrt


amicable_nums = {}

def sum_divisors(n: int) -> int:
    if n == 1:
        return 0
    dels = 1
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            dels += d
            q = n // d
            if q != d:
                dels += q
    return dels


ans = 0
for i in range(1, 10000):
    tmp = sum_divisors(i)
    if not tmp in amicable_nums.keys():
        amicable_nums[tmp] = [i]
    else:
        amicable_nums[tmp].append(i)

    if i in amicable_nums.keys():
        if tmp in amicable_nums[i] and tmp != i:
            ans += tmp + i
        
print(ans)