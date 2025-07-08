# 1
def get_uppers(mstr):
    for el in mstr:
        if el.isupper():
            yield el


a = get_uppers('Hello World!')

for el in a:
    print(el)


# 2
def get_longest_words(input_string):
    words = input_string.split()
    for word in words:
        if len(word) >= 4:
            yield word

input_string = "The quick brown fox jumps over the lazy dog"
longest_words = get_longest_words(input_string)

for word in longest_words:
    print(word)
