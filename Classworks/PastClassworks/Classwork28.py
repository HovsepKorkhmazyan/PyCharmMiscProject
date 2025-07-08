#1 Finding the longest words.

def split_line_into_words(line):
    return line.strip().split()

def find_longest_word(words):
    return max(words, key=len)

def process_file_contents(filename):
    longest_words = []
    with open(filename, 'r') as file:
        for line in file:
            words = split_line_into_words(line)
            if words:
                longest_words.append(find_longest_word(words))
    return longest_words

def print_results(longest_words):
    for i, word in enumerate(longest_words, start=1):
        print(f"Longest word in line {i}: {word}")

def main():
    filename = 'a.txt'
    longest_words = process_file_contents(filename)
    print_results(longest_words)

if __name__ == "__main__":
    main()

