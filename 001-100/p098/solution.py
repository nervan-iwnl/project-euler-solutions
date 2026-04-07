from math import isqrt
from collections import defaultdict
from itertools import combinations


def make_mapping(word, num):
    s = str(num)
    if len(word) != len(s):
        return None
    if s[0] == '0':
        return None

    letter_to_digit = {}
    digit_to_letter = {}

    for ch, d in zip(word, s):
        if ch in letter_to_digit:
            if letter_to_digit[ch] != d:
                return None
        else:
            letter_to_digit[ch] = d

        if d in digit_to_letter:
            if digit_to_letter[d] != ch:
                return None
        else:
            digit_to_letter[d] = ch

    if letter_to_digit[word[0]] == '0':
        return None

    return letter_to_digit


def apply_mapping(word, mapping):
    if mapping[word[0]] == '0':
        return None
    return int(''.join(mapping[ch] for ch in word))


def solve():
    with open("words.txt") as f:
        words = f.read().replace('"', '').split(',')

    groups = defaultdict(list)
    for word in words:
        groups[''.join(sorted(word))].append(word)

    anagram_groups = [group for group in groups.values() if len(group) >= 2]

    squares_by_len = defaultdict(list)
    square_sets_by_len = defaultdict(set)

    needed_lengths = set(len(group[0]) for group in anagram_groups)

    for length in needed_lengths:
        left = isqrt(10 ** (length - 1))
        if left * left < 10 ** (length - 1):
            left += 1
        right = isqrt(10 ** length - 1)

        for x in range(left, right + 1):
            sq = x * x
            squares_by_len[length].append(sq)
            square_sets_by_len[length].add(sq)
    ans = 0

    for group in anagram_groups:
        for w1, w2 in combinations(group, 2):
            length = len(w1)

            for sq in squares_by_len[length]:
                mapping = make_mapping(w1, sq)
                if mapping is None:
                    continue

                num2 = apply_mapping(w2, mapping)
                if num2 is None:
                    continue

                if num2 in square_sets_by_len[length]:
                    ans = max(ans, sq, num2)

    return ans


if __name__ == "__main__":
    print(solve())