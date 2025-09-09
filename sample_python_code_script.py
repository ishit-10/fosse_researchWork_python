""" This is a simple python code for implementing binary search.
    We use this code as the sameple student code to explore existing open source AI models by providing it as a prompt."""

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

numbers = [1, 3, 5, 7, 9, 11]
print(binary_search(numbers, 7))

#returns 3 (index of target value 7)
