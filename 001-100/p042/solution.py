from typing import List


def triangle_numbers(n: int) -> List[int]:
    return [i * (i + 1) // 2 for i in range(1, n + 1)]


def solve():
    with open('./001-100/p042/words.txt', 'r') as f:
        words = f.read().replace('"', '').split(',')

    triangle_numbers_list = triangle_numbers(3000)
    ans = 0
    for word in words:
        score = sum(ord(c) - ord('A') + 1 for c in word)
        if score in triangle_numbers_list:
            ans += 1    
    
    return ans

if __name__ == "__main__":
    print(solve())
