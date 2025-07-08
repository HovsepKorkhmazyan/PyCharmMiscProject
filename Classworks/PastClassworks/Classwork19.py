#1 Selection Sort
def selection_sort(arr):
    narr= []
    for i in range(len(arr)):
        si = find_smallest(arr)
        narr.append(arr.pop(si))
    return narr

def find_smallest(arr):
    smallest= arr[0]
    s_ind = 0
    for i in range(1,len(arr)):
        if arr[i] < smallest:
            smallest = arr[i]
            s_ind = i
    return s_ind

arr = [10,20,2,4,7,17,6]
print("Original array:", arr[:])
sorted_arr = selection_sort(arr)
print("Sorted array:", sorted_arr)


#2 Fibonacci with Recursion

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)

result = fib(10)
print(f"Fibonacci: {result}")

#3 Reverse Recursively

def reverse_string(s):
    if len(s) <= 1:
        return s
    return s[-1] + reverse_string(s[:-1])

input_string = "Hello, World!"
reversed_string = reverse_string(input_string)
print(f"Reversed string: {reversed_string}")

#4  Finding the sum of the digits of a given number recursively:
def sum_of_digits(n):
    if n == 0:
        return 0
    return n % 10 + sum_of_digits(n // 10)

number = 12
result = sum_of_digits(number)
print(f"Sum of {number} is : {result}")




