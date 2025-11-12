from functools import lru_cache 

coins = (1, 2, 5, 10, 20, 50, 100, 200)
amount = 200


@lru_cache(None)
def count_ways(amount, coins):
    if amount == 0:
        return 1
    if not coins:
        return 0
    
    curr = coins[0]
    ways = 0

    for i in range(0, amount // curr + 1):
        ways += count_ways(amount - i * curr, coins[1:])

    return ways


print(count_ways(amount, coins))