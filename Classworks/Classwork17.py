#1 Binary Search
ml = [2, 5, 7, 9, 11, 12, 15, 13, 20, 23]
sorted_ml = sorted(ml)
print(sorted_ml)

def binary_search(ml, target):
    first_index = 0
    last_index = len(ml) - 1
    while first_index <= last_index:
        mid_index = (first_index + last_index) // 2
        mid_value = ml[mid_index]
        if mid_value == target:
            return mid_index
        elif mid_value < target:
            first_index = mid_index + 1
        else:
            last_index = mid_index - 1
    return None

target = 4
result = binary_search(sorted_ml, target)

if result:
    print(f"Index Found {result}")
else:
    print(f"Index Not Found")

#2
def reverse_words(sentence):
    return ' '.join(word[::-1] for word in sentence.split())

def reverse_sentence(sentence):
    return sentence[::-1]

def title_case_words(sentence):
    return ' '.join(word.capitalize() for word in sentence.split())

def upper_case_words(sentence):
    return sentence.upper()

def vowels_upper_consonants_lower(sentence):
    vowels = "aeiouAEIOU"
    return ''.join(char.upper() if char in vowels else char.lower() for char in sentence)

def process_file(input_file, output_file):

    infile = open(input_file, 'r')
    sentences = infile.readlines()

    results = []
    for sentence in sentences:
        sentence = sentence.strip()
        results.append(reverse_words(sentence))
        results.append(reverse_sentence(sentence))
        results.append(title_case_words(sentence))
        results.append(upper_case_words(sentence))
        results.append(vowels_upper_consonants_lower(sentence))

    outfile = open(output_file, 'w')
    for result in results:
        outfile.write(result + '\n')


input_file = 'a.txt'
output_file = 'result.txt'


process_file(input_file, output_file)
print("Results saved to", output_file)
