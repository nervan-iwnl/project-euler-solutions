from itertools import combinations, permutations

'''
(o0, i0, i1,
 o1, i1, i2,
 o2, i2, i3,
 o3, i3, i4,
 o4, i4, i0)
'''

def solve():
    ans = -1
    for inner_combo in combinations(range(1, 11), 5):
        inner_combo = list(inner_combo)
        outer_combo = [n for n in range(1, 11) if n not in inner_combo]
        for inner in permutations(inner_combo):
            for outer in permutations(outer_combo):
                if outer[0] != min(outer):
                    continue
                target = outer[0] + inner[0] + inner[1]
                valid = True
                for k in range(1, 5):
                    s = outer[k] + inner[k] + inner[(k + 1) % 5]
                    if s != target:
                        valid = False
                        break
                if not valid:
                    continue
                
                res = ""
                for k in range(5):
                    res += str(outer[k]) + str(inner[k]) + str(inner[(k + 1) % 5])
                if len(res) == 16:
                    ans = max(ans, int(res))
    return ans



if __name__ == "__main__":
    print(solve())
