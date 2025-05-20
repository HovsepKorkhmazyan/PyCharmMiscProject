# 1
def get_content(fname):
    f = open(fname)
    return f.read()


def get_long_words(ml):
    return [e.strip() for e in ml if len(e) > 4]


content = get_content('a.txt')
longs = get_long_words(content)
print(longs)


# 2
def get_sentence_count(ml):
    return len(ml.split("."))


def get_words_count(ml):
    return len([el for el in ml.split() if el.isalpha])


def get_letter_count(ml):
    md = {}
    for el in ml:
        if el.isalpha():
            if el in md:
                md[el] += 1
            else:
                md[el] = 1
    return md


content = get_content('a.txt')
sen_count = get_sentence_count(content)
word_count = get_words_count(content)
letter_count = get_letter_count(content)
print("Sentence Count:", sen_count)
print("Word Count:", word_count)
print("Letter Count:", letter_count)

#3
def get_letter_count_alphabetically(ml):
    md = {}
    for el in ml:
        if el.isalpha():
            if el in md:
                md[el] += 1
            else:
                md[el] = 1
    f =open("result.txt", "w")
    for letter in sorted(md.keys()):
        f.write(f"{letter}: {md[letter]}\n")
    return md

words = get_content('a.txt')
letter_counts = get_letter_count_alphabetically(words)
print(letter_counts)

