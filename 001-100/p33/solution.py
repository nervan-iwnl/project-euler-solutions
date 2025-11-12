from math import gcd

num_prod = 1
den_prod = 1

for i in range(10, 100):
    for j in range(i + 1, 100):
        a, b = str(i), str(j)

        # ab / bc
        if a[1] == b[0] and a[1] != '0':
            new_num = int(a[0])
            new_den = int(b[1])

            if i * new_den == j * new_num:
                num_prod *= new_num
                den_prod *= new_den



g = gcd(num_prod, den_prod)
num_prod //= g
den_prod //= g

print(den_prod)
