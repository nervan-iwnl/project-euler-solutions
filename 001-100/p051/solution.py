from itertools import combinations


def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]


def solve():
    primes = sieve(1_000_000)
    
    prime_set = set(primes)
    
    for num in primes:
        if num < 10:
            continue
        
        s_num = str(num)
        
        for dig in '0123456789':
            positions = [i for i, ch in enumerate(s_num) if ch == dig]
            if not positions:
                continue
            
            for j in range(1, len(positions) + 1):
                for combo in combinations(positions, j):
                    ans = []
                    
                    for change in '0123456789':
                        if 0 in combo and change == '0':
                            continue
                        
                        s_num_arr = [i for i in s_num]
                        for idx in combo:
                            s_num_arr[idx] = change
                        
                        fam_num = int(''.join(s_num_arr))
                        if  fam_num < 1_000_000 and fam_num in prime_set:
                            ans.append(fam_num)
                            
                if len(ans) >= 8:
                    return min(ans)
    return None

if __name__ == "__main__":
    print(solve())
