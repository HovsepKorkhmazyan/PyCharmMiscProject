# 1. Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Selection Sort
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


numbers = [64, 25, 12, 22, 11]

sorted_selection = selection_sort(numbers.copy())
print("Selection Sort Result:", sorted_selection)

sorted_quick = quick_sort(numbers.copy())
print("Quick Sort Result:", sorted_quick)


# 2. Count Occurrences
def count_occurrences(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()

    number_counts = {}
    word_counts = {}

    for line in lines:
        line = line.strip()
        if line.isdigit():
            if line in number_counts:
                number_counts[line] += 1
            else:
                number_counts[line] = 1
        elif line:
            if line in word_counts:
                word_counts[line] += 1
            else:
                word_counts[line] = 1

    with open(output_file, 'w') as of:
        of.write("Number Counts:\n")
        for number, count in number_counts.items():
            of.write(f"{number}: {count}\n")

        of.write("\nWord Counts:\n")
        for word, count in word_counts.items():
            of.write(f"{word}: {count}\n")

# Example usage for counting occurrences
count_occurrences('words', 'counts.txt')


# 3. Sort Numbers by Sum of Digits
def sum_of_digits(n):
    return sum(int(digit) for digit in str(abs(n)))

numbers = []
while True:
    num = input("Enter a number (0 to stop): ")
    if num == '0':
        break
    else:
        numbers.append(int(num))


sorted_numbers = sorted(numbers, key=sum_of_digits)

output_file = 'sorted_counts.txt'
with open(output_file, 'w') as of:
    of.write("Number | Digit Sum\n")
    of.write("------------------\n")
    for num in sorted_numbers:
        of.write(f"{num:6} | {sum_of_digits(num)}\n")

print(f"\nResults written to {output_file}")


# 4. Recursive Function to Calculate Sum
def recursive_sum(numbers):
    if not numbers:
        return 0
    return numbers[0] + recursive_sum(numbers[1:])

# Example usage for recursive sum
total_sum = recursive_sum(numbers)
print(f"The sum of {numbers} is: {total_sum}")
