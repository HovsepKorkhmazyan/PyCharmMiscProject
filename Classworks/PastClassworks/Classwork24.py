# 1 Finding the sum with Try and Except:
def sum_numbers_in_file(file_path):
    total_sum = 0
    with open(file_path, 'r') as file:
        for line in file:
            try:
                total_sum += int(line.strip())
            except ValueError:
                pass
    return total_sum


file_path = 'a.txt'
result = sum_numbers_in_file(file_path)
print(f"{result}")


#2 Quick Sort Algorithm:

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)


arr = [3, 6, 8, 10, 1, 2, 1]
sorted_arr = quick_sort(arr)
print(f"Sorted array: {sorted_arr}")

#3

def word_count():
    counts = {}
    while True:
        word = input("Enter a word (type 'stop' to finish): ").strip()
        if word.lower() == 'stop':
            break
        try:
            counts[word] += 1
        except KeyError:
            counts[word] = 1 

    print("\nWord counts:")
    for word, count in counts.items():
        print(f"{word}: {count}")

word_count()





