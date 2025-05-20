def display_hidden_word(question, hidden_word):
    print(f"{question} {hidden_word}")


def update_hidden_word(answer, hidden_word, user_answer):
    for i in range(len(answer)):
        if answer[i] == user_answer:
            hidden_word = hidden_word[:i] + user_answer + hidden_word[i + 1:]
    return hidden_word


def play_game():
    question = "Who invented Python programming language?"
    answer = "Guido van Rossum"
    hidden_word = ''.join('-' if i != ' ' else ' ' for i in answer)
    attempts = 6

    while hidden_word != answer and "-" in hidden_word:
        display_hidden_word(question, hidden_word)
        user_answer = input("Enter a letter or the answer: ")

        if user_answer == answer:
            hidden_word = answer
            print(f"Your answer is CORRECT: {hidden_word}")
            break

        if len(user_answer) == 1:
            if user_answer in answer:
                hidden_word = update_hidden_word(answer, hidden_word, user_answer)
                print("Good guess!")
            else:
                print("Wrong Letter")
                attempts -= 1
                print(f"You have {attempts} attempts left.")
                if attempts == 0:
                    print(f"Game Over! The correct answer is {answer}")
                    break
        elif len(user_answer) > 1:
            print("Please enter only one letter or the full answer.")

        if hidden_word == answer:
            print(f"Congratulations! You've guessed the word: {hidden_word}")
            break


if __name__ == "__main__":
    play_game()
