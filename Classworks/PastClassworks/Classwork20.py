#1
def load_dictionary(filename):
    dictionary = {}

    with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    english_word, translation = parts
                    dictionary[english_word.lower()] = translation
            return dictionary

def save_translation(filename, word, translation):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{word} {translation}\n")

def replace_word(word, translation):
    stripped_word = word.strip('.,!?;:"\'')
    prefix = word[:word.find(stripped_word)] if word.find(stripped_word) != -1 else ''
    suffix = word[word.find(stripped_word) + len(stripped_word):] if word.find(stripped_word) != -1 else ''
    return prefix + translation + suffix

def translate_sentence(sentence, dictionary, filename):
    words = sentence.split()
    translated_words = []
    for word in words:
        stripped_word = word.strip('.,!?;:"\'').lower()
        translation = dictionary.get(stripped_word, None)
        if translation:
            new_word = replace_word(word, translation)
            translated_words.append(new_word)
        else:
            user_translation = input(f"Please provide the translation for '{stripped_word}': ").strip()
            if user_translation:
                dictionary[stripped_word] = user_translation
                save_translation(filename, stripped_word, user_translation)
                new_word = replace_word(word, user_translation)
                translated_words.append(new_word)
            else:
                translated_words.append(word)
    return ' '.join(translated_words)

def main():
    filename = 'a.txt'
    dictionary = load_dictionary(filename)
    sentence = input("Enter a sentence to translate: ")
    translated = translate_sentence(sentence, dictionary, filename)
    print("Translated sentence:")
    print(translated)

main()

#2
temp_ls=[11,2,4,3,7,8,10,6]
def write_numbers(filename, numbers):
    with open(filename, 'w') as f:
        for number in numbers:
            f.write(str(number) + '\n')

def read_numbers(filename):
    numbers = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.isdigit():
                numbers.append(int(line))
    return numbers

def write_odd_even(filename, numbers):
    odd_numbers = [str(n) for n in numbers if n % 2 != 0]
    even_numbers = [str(n) for n in numbers if n % 2 == 0]
    with open(filename, 'w') as f:
        f.write("Odd numbers:\n")
        f.write('\n'.join(odd_numbers) + '\n')
        f.write("Even numbers:\n")
        f.write('\n'.join(even_numbers) + '\n')

def main():
    temp_ls = [11, 2, 4, 3, 7, 8, 10, 6]
    write_numbers('numbers.txt', temp_ls)
    numbers = read_numbers('numbers.txt')
    write_odd_even('results.txt', numbers)


main()
