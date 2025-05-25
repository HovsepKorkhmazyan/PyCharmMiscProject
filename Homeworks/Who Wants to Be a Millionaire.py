import random
import os


def read_questions_from_file(filename):
    questions = []
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    blocks = content.split('\n\n')

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue
        question = lines[0].strip()
        answers = [line.strip() for line in lines[1:] if line.strip()]
        if len(answers) < 2:
            continue
        questions.append((question, answers))
    return questions


def shuffle_questions(questions):
    random.shuffle(questions)
    return questions


def get_shuffled_answers(correct_answer, wrong_answers):
    sample_size = min(3, len(wrong_answers))
    random_wrong = random.sample(wrong_answers, sample_size)
    answer_options = random_wrong + [correct_answer]
    random.shuffle(answer_options)
    return answer_options


def ask_question(question, shuffled_answers, correct_answer):
    print(question)
    for i, answer in enumerate(shuffled_answers):
        print(f"{i + 1}. {answer}")
    user_answer = input("Please select the correct answer: ")
    if user_answer.isdigit() and 1 <= int(user_answer) <= len(shuffled_answers) and shuffled_answers[
        int(user_answer) - 1] == correct_answer:
        print("Correct!\n")
        return True
    else:
        print("Incorrect. The correct answer was:", correct_answer, "\n")
        return False


def quiz(questions):
    score = 0
    questions = shuffle_questions(questions)
    for question, answers in questions:
        correct_answer = answers[0]
        wrong_answers = answers[1:]
        shuffled_answers = get_shuffled_answers(correct_answer, wrong_answers)

        if ask_question(question, shuffled_answers, correct_answer):
            score += 1

    print(f"Your final score is: {score}/{len(questions)}")
    return score


def add_question_to_file(filename):
    question = input("Enter the question: ")
    answers = []
    for i in range(4):
        answer = input(f"Enter answer {i + 1}: ")
        answers.append(answer)
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{question}\n" + "\n".join(answers) + "\n\n")
    print("Question added successfully!")


#Main Logic
    filename = "questions"
    scores = {}

    while True:
        username = input("Enter your username: ")
        if username in scores:
            print("Username already exists. Please try again.")
        else:
            scores[username] = 0
            break

    while True:
        choice = input("Do you want to play(p)  or add(a) a question? (q to quit): ").lower()
        if choice == 'p':
            questions = read_questions_from_file(filename)
            if questions:
                score = quiz(questions)
                scores[username] += score
                print(f"{username}'s total score: {scores[username]}")
            else:
                print("No valid questions found in the file.")
        elif choice == 'a':
            add_question_to_file(filename)
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please select 'p', 'a', or 'q'.")


    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("\nScores:")
    for user, score in sorted_scores:
        print(f"{user}: {score}")

