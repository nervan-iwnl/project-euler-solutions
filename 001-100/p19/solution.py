ans = 0

month_days = [31,28,31,30,31,30,31,31,30,31,30,31]


curr_day = 0
for i in range(12):
    curr_day += month_days[i]
    curr_day %= 7

for i in range(1901, 2001):
    for j in range(12):
        if curr_day == 6:
            ans += 1
        curr_day += month_days[j]
        if j == 1 and ((i % 100 != 0 and i % 4 == 0) or (i % 400 == 0)):
            curr_day += 1
        curr_day %= 7

print(ans)