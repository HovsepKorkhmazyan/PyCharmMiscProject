import random

# Palindrome and Word Functions
def is_palindrome(num_str):
    return num_str == num_str[::-1]


def add_palindrome(palindromes, num_str, filepath="result.txt"):
    palindromes.append(int(num_str))
    palindromes.sort()
    with open(filepath, "w") as f:
        for num in palindromes:
            f.write(str(num) + "\n")


def is_word(word):
    return word.isalpha()


def write_words_alphabetically(words, filepath="words_alpha.txt"):
    sorted_words = sorted(words)
    with open(filepath, "w") as f:
        for word in sorted_words:
            f.write(word + "\n")


def write_words_by_length(words, filepath="words_length.txt"):
    sorted_words = sorted(words, key=len)
    with open(filepath, "w") as f:
        for word in sorted_words:
            f.write(str(word) + "\n")


def get_data():
    return {
        "words": [],
        "numbers": []
    }


def create_sum_dict(words):
    tmp = {}
    for el in words:
        tmp[el] = sum(ord(v) for v in el)
    return tmp


# Game Functions
def get_username():
    return input("Enter your username: ").strip()


def ask_question(country, capital):
    answer = input(f"What is the capital of {country}? ").strip()
    return answer.lower() == capital.lower()


def play_game(countries_and_capitals, attempts=5):
    score = 0
    countries = list(countries_and_capitals.keys())
    asked_countries = set()
    questions_asked = 0

    while questions_asked < attempts:
        country = random.choice(countries)
        if country in asked_countries:
            continue

        asked_countries.add(country)
        capital = countries_and_capitals[country]

        if ask_question(country, capital):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer is {capital}.")

        questions_asked += 1

    return score


def save_score(username, score, filepath="top.txt"):
    with open(filepath, "a") as f:
        f.write(f"{username} - {str(score)}\n")


def get_questions():
    return {
        "France": "Paris",
        "Germany": "Berlin",
        "Italy": "Rome",
        "Spain": "Madrid",
        "Portugal": "Lisbon",
        "Canada": "Ottawa",
        "Japan": "Tokyo",
        "Australia": "Canberra",
        "India": "New Delhi",
        "Brazil": "Brasilia"
    }


def main():
    data = get_data()
    words = data["words"]
    numbers = data["numbers"]
    palindromes = []

    while True:
        user_input = input("Enter a number or word (or 'stop' to exit): ")
        if user_input == "stop":
            print("Exiting.")
            break
        if user_input.isdigit():
            numbers.append(int(user_input))
            if is_palindrome(user_input):
                add_palindrome(palindromes, user_input)
                print(f"{user_input} is a palindrome and has been written to result.txt.")
            else:
                print(f"{user_input} is not a palindrome.")
        elif is_word(user_input):
            words.append(user_input)
            write_words_alphabetically(words)
            write_words_by_length(words)
            print(f"Words written to words_alpha.txt")
        else:
            print(f"Invalid input")

    # Capital City Game
    countries_and_capitals = get_questions()
    username = get_username()
    score = play_game(countries_and_capitals)
    print(f"Game over! {username}, your score is {score} out of 5.")
    save_score(username, score)
