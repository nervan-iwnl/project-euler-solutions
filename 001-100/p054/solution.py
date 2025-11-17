from typing import List


values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
          '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

suits = {'H', 'D', 'C', 'S'}


def is_flush(cards: List[str]) -> bool:
    return len({card[1] for card in cards}) == 1


def card_ranks(cards: List[str]) -> List[int]:
    ranks = sorted((values[i[0]] for i in cards), reverse=True)
    return ranks
    

def is_straight(cards: List[str]) -> bool:
        return len(set(card_ranks(cards))) == 5 and card_ranks(cards)[0] - card_ranks(cards)[4] == 4 

    

def hand_value(cards):
    """
    8: straight flush
    7: four of a kind
    6: full house
    5: flush
    4: straight
    3: three of a kind
    2: two pairs
    1: one pair
    0: high card
    """
    ranks = card_ranks(cards)

    map_cards = {}
    for i in ranks: 
        if i in map_cards.keys():
            map_cards[i] += 1
        else:
            map_cards[i] = 1
            
    if is_flush(cards) and is_straight(cards): # straight flush
        return (8, max(ranks))
    
    if sorted(map_cards.values()) == [1, 4]: # four of a kind
        for i in map_cards.keys():
            if map_cards[i] == 4:
                return (7, i)
    
    if sorted(map_cards.values()) == [2, 3]: # full house
        for i in map_cards.keys():
            if map_cards[i] == 3:
                return (6, i)
            
    if is_flush(cards): # flush
        return (5, ranks[0])
    
    if is_straight(cards): # street
        return (4, ranks[0])
    
    if 3 in map_cards.values(): # tree of a kind
        for i in map_cards.keys():
            if map_cards[i] == 3:
                return (3, i)

    if sorted(map_cards.values()) == [1, 2, 2]: # two pair
        solo_rank = -1
        couple_ranks = []
        for i in map_cards.keys():
            if map_cards[i] == 1:
                solo_rank = i
            else:
                couple_ranks.append(i)
        return (2, max(couple_ranks), min(couple_ranks), solo_rank)

    if 2 in map_cards.values(): # pair
        solo_ranks = []
        couple_rank = -1
        for i in map_cards.keys():
            if map_cards[i] == 2:
                couple_rank = i
            else:
                solo_ranks.append(i)
        return (1, couple_rank, sorted(solo_ranks)[::-1])
    
    return (0, sorted(map_cards.keys())[::-1]) # high card

    
    
    

def solve():
    ans = 0
    with open('./poker.txt', 'r') as f:

        for line in f:
            line = line.strip()
            if not line:
                continue
            
            combinations = line.split()
            player1 = combinations[:5]
            player2 = combinations[5:]
            if hand_value(player1) > hand_value(player2):
                ans += 1

    return ans

if __name__ == "__main__":
    print(solve())
