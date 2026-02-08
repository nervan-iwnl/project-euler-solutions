with open("src/001-100/p079/keylog.txt") as f:
    keylog = f.read().splitlines()

graph = {i : set() for i in range(10)}

for code in keylog:
    graph[int(code[0])].add(int(code[1]))
    graph[int(code[1])].add(int(code[2]))
    graph[int(code[0])].add(int(code[2]))


def solve():
    ans = ''
    grp = sorted(graph, key=lambda x: len(graph[x]))
    if_was = graph[max(graph, key=lambda x: len(graph[x]))] | {max(graph, key=lambda x: len(graph[x]))}
    for i in grp:
        if i in if_was:
            ans += str(i)
    return ans[::-1]


if __name__ == "__main__":
    print(solve())
