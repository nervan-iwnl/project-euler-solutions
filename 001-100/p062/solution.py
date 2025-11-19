def solve():
    cube_d = {}
    min_cube = 10**20
    for i in range(1, 1_000_000):
        num = i**3
        key = ''.join(sorted(str(num)))
        cube_d.setdefault(key, [0, i**3])[0] += 1
        if cube_d[key][0] >= 5:
            min_cube = min(min_cube, cube_d[key][1])
    
    return min_cube

if __name__ == "__main__":
    print(solve())
