import argparse
import string
from collections import Counter


def load_stop_words():
    return {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
            'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they',
            'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
            'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
            'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
            'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
            'can', 'will', 'just', 'don', 'should', 'now'}


def count_word_frequencies(file_path, top_n):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()

    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()

    stop_words = load_stop_words()
    filtered_words = [word for word in words if word not in stop_words]

    word_counts = Counter(filtered_words)
    return word_counts.most_common(top_n)


def main():
    parser = argparse.ArgumentParser(description='Count word frequencies in a text file.')
    parser.add_argument('file_path', type=str, help='Path to the text file to analyze.')
    parser.add_argument('top_n', type=int, help='Number of top frequent words to display.')

    args = parser.parse_args()

    top_words = count_word_frequencies(args.file_path, args.top_n)

    for word, frequency in top_words:
        print(f'{word}: {frequency}')


if __name__ == '__main__':
    main()
