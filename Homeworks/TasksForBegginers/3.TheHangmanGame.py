try:
    import random
    import argparse
except ImportError as e:
    print(f"Import error: {e}")



def select_word():
    words = ['python', 'hangman', 'programming', 'computer', 'keyboard',
             'developer', 'algorithm', 'function', 'variable', 'dictionary']
    return random.choice(words).lower()

def display_hangman(incorrect_guesses, show_art):
    hangman_art = [
        """
          +---+
          |   |
              |
              |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
              |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
          |   |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|   |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
         /    |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
         / \\  |
              |
        =========
        """
    ]
    if show_art:
        print(hangman_art[min(incorrect_guesses, len(hangman_art) - 1)])

def process_guess(guess, secret_word, guessed_letters, word_progress):
    if guess in secret_word:
        print(f"Correct! '{guess}' is in the word.")
        for i, letter in enumerate(secret_word):
            if letter == guess:
                word_progress[i] = guess
    else:
        print(f"Sorry, '{guess}' is not in the word.")
        return False
    return True

def check_game_status(word_progress, incorrect_guesses, max_attempts, secret_word):
    if '_' not in word_progress:
        print("\nCongratulations! You guessed the word:", secret_word)
        return True
    if incorrect_guesses >= max_attempts:
        print("\nGame over! The word was:", secret_word)
        return True
    return False

def hangman(max_attempts, show_art):
    secret_word = select_word()
    guessed_letters = set()
    incorrect_guesses = 0
    word_progress = ['_'] * len(secret_word)

    print("Welcome to Hangman!")
    print(f"The word has {len(secret_word)} letters.")
    print(' '.join(word_progress))

    while True:
        guess = input("\nGuess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You've already guessed that letter!")
            continue

        guessed_letters.add(guess)

        if not process_guess(guess, secret_word, guessed_letters, word_progress):
            incorrect_guesses += 1
            display_hangman(incorrect_guesses, show_art)
            print(f"You have {max_attempts - incorrect_guesses} attempts left.")

        print("\nWord: ", ' '.join(word_progress))
        print("Guessed letters: ", sorted(guessed_letters))

        if check_game_status(word_progress, incorrect_guesses, max_attempts, secret_word):
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Hangman Game")
    parser.add_argument("-a", "--attempts", type=int, default=6, help="Maximum number of incorrect attempts allowed")
    parser.add_argument("-s", "--show_art", action='store_true', help="Display hangman art during the game")

    args = parser.parse_args()

    hangman(args.attempts, args.show_art)
