def next_permutation(nums):
    i = j = len(nums) - 1
    while i > 0 and nums[i - 1] >= nums[i]:
        i -= 1
    if i == 0:
        return nums[::-1]
    
    while nums[j] <= nums[i - 1]:
        j -= 1

    nums[i - 1], nums[j] = nums[j], nums[i - 1]
    nums[i:] = reversed(nums[i:])
    return nums




arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

for i in range(1_000_000 - 1):
    arr = next_permutation(arr)
    
for i in arr:
    print(i, end='')