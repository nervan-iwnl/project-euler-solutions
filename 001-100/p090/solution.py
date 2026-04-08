from itertools import combinations 

def extend(cube):
    s = set(cube)
    if 6 in s or 9 in s:
        s.add(6)
        s.add(9)
    return s


def solve():
    sq = [((i * i) // 10, (i * i) % 10) for i in range(1, 10)]
    digits = range(10)
    ans = 0
    cubes = list(combinations(digits, 6))
    for i in range(len(cubes)):
        for j in range(i, len(cubes)):
            cube1 = extend(cubes[i])
            cube2 = extend(cubes[j])
            ans += 1
            for a, b in sq:
                if not ((a in cube1 and b in cube2) or (a in cube2 and b in cube1)):
                    ans -= 1
                    break
            

    return ans

if __name__ == "__main__":
    print(solve())
