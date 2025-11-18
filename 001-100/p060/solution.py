from typing import List

def sieve(n: int) -> List[int]:
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    limit = int(n ** 0.5)
    for p in range(2, limit + 1):
        if is_prime[p]:
            start = p * p
            step = p
            is_prime[start:n + 1:step] = [False] * (((n - start) // step) + 1)

    return [i for i, ok in enumerate(is_prime) if ok]



def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def concat(a: int, b: int):
    return is_prime(int(str(a) + str(b))) and is_prime(int(str(b) + str(a)))


k = 5
best_sum = 10**15
best_clique = None

primes = sieve(10000)
graph = {i : [] for i in primes}

def dfs(clique, candidates):
    global best_sum, best_clique
    
    
    if len(clique) == k:
        if sum(clique) <= best_sum:
            best_clique = clique[:]
            best_sum = sum(clique)
        return    
    
    if len(clique) + len(candidates) < k:
        return

    
    for idx, v in enumerate(candidates):
        new_candidates = []
        for u in candidates[idx + 1:]:
            ok = True
            if u not in graph[v]:
                ok = False
            else:
                for q in clique:
                    if u not in graph[q]:
                        ok = False
                        break
            if ok:
                new_candidates.append(u)

        dfs(clique + [v], new_candidates)


    


def solve():
    for i in range(len(primes)):
        a = primes[i]
        for j in range(i + 1, len(primes)):
            b = primes[j]
            if concat(a, b):
                graph[a].append(b)
                graph[b].append(a)
    dfs([], primes)
    return best_clique, best_sum

if __name__ == "__main__":
    print(solve())
