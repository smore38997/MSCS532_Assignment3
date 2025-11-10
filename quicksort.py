import random

def randomized_quicksort(arr):
   

    if len(arr) <= 1:
        return arr


    pivot = random.choice(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]

    return randomized_quicksort(less) + equal + randomized_quicksort(greater)




    # Empty array
print(randomized_quicksort([]))

    # Single element
print(randomized_quicksort([42]))  

    # Already sorted array
print(randomized_quicksort([1, 2, 3, 4, 5]))  

    # Reverse sorted array
print(randomized_quicksort([5, 4, 3, 2, 1]))  
    # Array with duplicates
print(randomized_quicksort([3, 6, 3, 2, 7, 2, 2, 5])) 

    # Random array
print(randomized_quicksort([10, -1, 0, 5, 2, 10, 3]))  