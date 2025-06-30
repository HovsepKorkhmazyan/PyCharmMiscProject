import random
import argparse


def hangman(max_attempts, show_art):
    words = ['python', 'hangman', 'programming', 'computer', 'keyboard',
             'developer', 'algorithm', 'function', 'variable', 'dictionary']

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

    secret_word = random.choice(words).lower()
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

        if guess in secret_word:
            print(f"Correct! '{guess}' is in the word.")
            for i, letter in enumerate(secret_word):
                if letter == guess:
                    word_progress[i] = guess
        else:
            incorrect_guesses += 1
            print(f"Sorry, '{guess}' is not in the word.")
            if show_art:
                print(hangman_art[min(incorrect_guesses, len(hangman_art) - 1)])
            print(f"You have {max_attempts - incorrect_guesses} attempts left.")

        print("\nWord: ", ' '.join(word_progress))
        print("Guessed letters: ", sorted(guessed_letters))

        if '_' not in word_progress:
            print("\nCongratulations! You guessed the word:", secret_word)
            break

        if incorrect_guesses >= max_attempts:
            print("\nGame over!")
            if show_art:
                print(hangman_art[-1])
            print("The word was:", secret_word)
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Hangman Game")
    parser.add_argument("-a", "--attempts", type=int, default=6, help="Maximum number of incorrect attempts allowed")
    parser.add_argument("-s", "--show_art", action='store_true', help="Display hangman art during the game")

    args = parser.parse_args()

    hangman(args.attempts, args.show_art)
