nums = {
    0: '',
    1: 'one',   2: 'two',     3: 'three', 4: 'four',  5: 'five',
    6: 'six',   7: 'seven',   8: 'eight', 9: 'nine',  10: 'ten',
    11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen',
    16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen',
    20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty',
    60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety',
    100: 'hundred', 1000: 'thousand'
}

AND = 'and'


def parse_let(n: int) -> int:
    if n == 1000:
        return len(nums[1]) + len(nums[1000])

    if n >= 100:
        h = n // 100
        rest = n % 100
        res = len(nums[h]) + len(nums[100]) 
        if rest:
            res += len(AND) + parse_let(rest)
        return res

    if n >= 20:
        t = (n // 10) * 10
        u = n % 10
        return len(nums[t]) + (len(nums[u]) if u else 0)

    return len(nums[n])
        
        

ans = 0

for i in range(1, 1001):
    ans += parse_let(i)
    
print(ans)