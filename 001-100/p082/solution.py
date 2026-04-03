def solve():
    matrix = []
    with open('matrix.txt') as f:
        for line in f.readlines():
            matrix.append([int(i) for i in line.split(',')])
    ans = [[matrix[i][0]] for i in range(len(matrix))]
    n = len(matrix)
    for j in range(1, n):
        for i in range(n):
            ans[i].append(ans[i][j - 1] + matrix[i][j])
            
        for i in range(1, n):
            ans[i][j] = min(ans[i][j], ans[i-1][j] + matrix[i][j]) 

        for i in range(n-2, -1, -1):
            ans[i][j] = min(ans[i][j], ans[i+1][j] + matrix[i][j])
    
    return min([ans[i][-1] for i in range(n)])
    
    
if __name__ == "__main__":
    print(solve())
