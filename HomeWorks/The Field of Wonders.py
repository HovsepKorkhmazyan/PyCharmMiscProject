question = "Who invented Python programming language"
answer = "Guido van Rossum"
hidden_word = ''.join('-' if i != ' ' else ' ' for i in answer)
attempts = 6

while hidden_word != answer or "-" not in hidden_word:
    print(f"{question} {hidden_word}")
    user_answer = input("Enter a letter or the answer: ")

    if user_answer == answer:
        hidden_word = answer
        print(f"Your answer is CORRECT: {hidden_word}")
        break

    if len(user_answer) >= 1:
        if user_answer in answer:
            for i in range(len(answer)):
                if answer[i] == user_answer:
                    hidden_word = hidden_word[:i] + user_answer + hidden_word[i + 1:]
            print("Good guess!")
        else:
            print("Wrong Letter")
            attempts -= 1
            print(f"You have {attempts} attempts left.")
            if attempts == 0:
                print(f"Game Over! The correct answer is {answer}")
                break
    else:
        print("Please enter only one letter or the full answer.")

    if hidden_word == answer:
        print(f"Congratulations! You've guessed the word: {hidden_word}")
        break
