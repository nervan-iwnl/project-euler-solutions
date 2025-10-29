arr = [[0] * 21 for _ in range(21)]

arr[0][0] = 1

for i in range(21):
    for j in range(21):
        if i > 0:
            arr[i][j] += arr[i - 1][j]
        if j > 0:
            arr[i][j] += arr[i][j - 1]
            
print(arr[-1][-1])