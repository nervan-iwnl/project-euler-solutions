from itertools import product


def decrypt_codes(codes: list[int], key: str) -> str:
    key_bytes = [ord(c) for c in key]
    klen = len(key_bytes)
    res = []
    for i, val in enumerate(codes):
        res.append(chr(val ^ key_bytes[i % klen]))
    return ''.join(res)


def solve():
    with open('cipher.txt', 'r') as f:
        ct = [int(x) for x in f.read().strip().split(',')]

    for a, b, c in product(range(ord('a'), ord('z') + 1), repeat=3):
        key = chr(a) + chr(b) + chr(c)
        if decrypt_codes(ct, key).count(' ') > 200 and " the " in decrypt_codes(ct, key).lower(): 
            txt = decrypt_codes(ct, key)
            return sum([ord(i) for i in txt])
                
    return None

if __name__ == "__main__":
    print(solve())
