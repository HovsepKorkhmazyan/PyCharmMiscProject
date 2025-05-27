import random
import os

def read_file_content(filename):
    """Reads the content of the specified file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip()

def parse_questions(content):
    """Parses the content into a list of questions and answers."""
    questions = []
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

def read_questions_from_file(filename):
    """Reads and parses questions from a specified file."""
    content = read_file_content(filename)
    return parse_questions(content)

def shuffle_questions(questions):
    """Shuffles the list of questions."""
    random.shuffle(questions)
    return questions

def get_shuffled_answers(correct_answer, wrong_answers):
    """Generates a shuffled list of answer options including the correct answer."""
    sample_size = min(3, len(wrong_answers))
    random_wrong = random.sample(wrong_answers, sample_size)
    answer_options = random_wrong + [correct_answer]
    random.shuffle(answer_options)
    return answer_options

def display_question_with_answers(question, shuffled_answers):
    """Displays the question and its possible answers."""
    print(question)
    for i, answer in enumerate(shuffled_answers):
        print(f"{i + 1}. {answer}")

def get_user_answer(num_options):
    """Prompts the user for an answer and validates the input."""
    user_answer = input("Please select the correct answer: ")
    if user_answer.isdigit() and 1 <= int(user_answer) <= num_options:
        return int(user_answer)
    return None

def ask_question(question, shuffled_answers, correct_answer):
    """Asks the user a question and checks if the answer is correct."""
    display_question_with_answers(question, shuffled_answers)
    user_choice = get_user_answer(len(shuffled_answers))
    if user_choice and shuffled_answers[user_choice - 1] == correct_answer:
        print("Correct!\n")
        return True
    else:
        print("Incorrect. The correct answer was:", correct_answer, "\n")
        return False

def quiz(questions):
    """Conducts a quiz using the provided questions."""
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
    """Adds a new question and its answers to the specified file."""
    question = input("Enter the question: ")
    answers = []
    for i in range(4):
        answer = input(f"Enter answer {i + 1}: ")
        answers.append(answer)
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{question}\n" + "\n".join(answers) + "\n\n")
    print("Question added successfully!")

def get_unique_username(scores):
    """Prompts the user for a unique username."""
    while True:
        username = input("Enter your username: ")
        if username in scores:
            print("Username already exists. Please try again.")
        else:
            return username

def prompt_user_choice():
    """Prompts the user to choose an action."""
    return input("Do you want to play (p) or add (a) a question? (q to quit): ").lower()

def display_scores(scores):
    """Displays the scores of all users."""
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("\nScores:")
    for user, score in sorted_scores:
        print(f"{user}: {score}")

def main():
    """Main function to run the quiz application."""
    filename = "questions"
    scores = {}
    username = get_unique_username(scores)
    scores[username] = 0

    while True:
        choice = prompt_user_choice()
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
    display_scores(scores)

if __name__ == "__main__":
    main()

