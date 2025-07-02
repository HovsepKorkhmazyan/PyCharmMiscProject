from Questions import Questions
from Player import Player

def main():
    quiz = Questions("questions")
    player = Player("")

    username = player.get_unique_username()
    player.username = username
    player.scores[username] = 0

    while True:
        choice = player.prompt_user_choice()

        if choice == 'p':
            quiz.shuffle()
            for question, answers in quiz.questions:
                player.ask_question(question, answers)
            player.display_score()
            player.scores[player.username] = player.score

        elif choice == 'a':
            question = input("Enter the question: ")
            answers = [input(f"Enter answer {i + 1}: ") for i in range(4)]
            quiz.add_question(question, answers)

        elif choice == 'q':
            break

    player.display_all_scores()
    player.save_scores_to_file()

if __name__ == "__main__":
    main()
