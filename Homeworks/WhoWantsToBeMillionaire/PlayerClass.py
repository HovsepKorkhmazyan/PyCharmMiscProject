import random

class Player:
    def __init__(self, username):
        self.username = username
        self.score = 0
        self.scores = {}

    def prompt_user_choice(self):

        while True:
            choice = input("Do you want to play (p) or add (a) a question? (q to quit): ").lower()
            if choice in ['p', 'a', 'q']:
                return choice
            print("Invalid choice. Please select 'p', 'a', or 'q'.")

    def get_unique_username(self):

        while True:
            username = input("Enter your username: ")
            if username in self.scores:
                print("Username already exists. Please try again.")
            else:
                return username

    def ask_question(self, question, answers):

        question_text, answer_options = question, answers
        correct_answer = answer_options[0]
        wrong_answers = answer_options[1:]
        shuffled_answers = random.sample(wrong_answers, min(3, len(wrong_answers))) + [correct_answer]
        random.shuffle(shuffled_answers)

        print(question_text)
        for i, answer in enumerate(shuffled_answers):
            print(f"{i + 1}. {answer}")

        user_choice = self._get_user_answer(len(shuffled_answers))
        if shuffled_answers[user_choice - 1] == correct_answer:
            print("Correct!\n")
            self.score += 1
            return True
        print("Incorrect. The correct answer was:", correct_answer, "\n")
        return False

    def _get_user_answer(self, num_options):

        while True:
            answer = input("Please select the correct answer (1-{}): ".format(num_options))
            if answer.isdigit() and 1 <= int(answer) <= num_options:
                return int(answer)
            print("Invalid input. Please enter a number between 1 and", num_options)

    def display_score(self):

        print(f"{self.username}'s score: {self.score}")

    def display_all_scores(self):

        print("\nLeaderboard:")
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (user, score) in enumerate(sorted_scores, 1):
            print(f"{rank}. {user}: {score}")
