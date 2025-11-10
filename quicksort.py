import random

def randomized_quicksort(arr):
    """
    Sorts the input list using Randomized Quicksort algorithm.
    Handles empty lists, duplicates, and already-sorted arrays efficiently.
    """

    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr

    # Choose a random pivot
    pivot = random.choice(arr)

    # Partition into three parts:
    #   less: elements less than pivot
    #   equal: elements equal to pivot (for duplicates)
    #   greater: elements greater than pivot
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]

    # Recursively sort subarrays and combine
    return randomized_quicksort(less) + equal + randomized_quicksort(greater)



