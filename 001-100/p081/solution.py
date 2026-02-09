with open('matrix.txt') as f:
    matrix = [[int(x) for x in line.split(',')] for line in f]
    
    
ans = [[0] * len(matrix[0]) for _ in range(len(matrix))]

ans[0][0] = matrix[0][0]

for i in range(1, len(matrix)):
    ans[i][0] = ans[i-1][0] + matrix[i][0]
    
for j in range(1, len(matrix[0])):
    ans[0][j] = ans[0][j-1] + matrix[0][j]
    
for i in range(1, len(matrix)):
    for j in range(1, len(matrix[0])):
        ans[i][j] = min(ans[i-1][j], ans[i][j-1]) + matrix[i][j]
        
print(ans[-1][-1])