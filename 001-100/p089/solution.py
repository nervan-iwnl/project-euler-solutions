values = {
    'M': 1000,
    'CM': 900,
    'D': 500,
    'CD': 400,
    'C': 100,
    'XC': 90,
    'L': 50,
    'XL': 40,
    'X': 10,
    'IX': 9,
    'V': 5,
    'IV': 4,
    'I': 1
}

def from_roman(string: str):
    ans = 0
    for i, el in enumerate(string):
        if i + 1 < len(string) and values[el] < values[string[i + 1]]:
            ans -= values[el]
        else:
            ans += values[el]
    return ans


def to_roman(num: int):
    values = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I')
    ]
    ans = ''
    curr = 0
    while num > 0:
        rom, string = values[curr] 
        if num < rom:
            curr += 1
            continue
        ans += string
        num -= rom
    return ans

def solve():
    ans = 0
    with open('roman.txt') as f:
        for line in f.readlines():
            line = line.strip()
            ans += len(line) - len(to_roman(from_roman(line)))
            #print(line, from_roman(line), to_roman(from_roman(line)))
        
    return ans 

if __name__ == "__main__":
    print(solve())
