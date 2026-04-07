import heapq

def solve():
    matrix = []
    with open('matrix.txt') as f:
        for line in f:
            matrix.append(list(map(int, line.strip().split(','))))
    
    n = len(matrix)
    m = len(matrix[0])
    INF = 10**18
    dist = [[INF] * m for _ in range(n)]
    dist[0][0] = matrix[0][0]
    pq = [(matrix[0][0], 0, 0)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while pq:
        curr_dist, r, c = heapq.heappop(pq)
        
        if curr_dist != dist[r][c]:
            continue
        
        if r == n - 1 and c == m - 1:
            return curr_dist
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < n and 0 <= nc < m:
                new_dist = curr_dist + matrix[nr][nc]
                
                if new_dist < dist[nr][nc]:
                    dist[nr][nc] = new_dist
                    heapq.heappush(pq, (new_dist, nr, nc))
    return None


if __name__ == "__main__":
    print(solve())
