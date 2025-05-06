import random

questions = [
    ("What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"]),
    ("What is 2 + 2?", ["4", "3", "5", "6"]),
    ("What is the largest planet in our solar system?", ["Jupiter", "Earth", "Mars", "Saturn"]),
    ("What is the chemical symbol for water?", ["H2O", "O2", "CO2", "NaCl"]),
    ("Who wrote 'Romeo and Juliet'?", ["William Shakespeare", "Charles Dickens", "Mark Twain", "Jane Austen"]),
    ("What is the smallest prime number?", ["2", "1", "3", "4"]),
    ("What is the currency of Japan?", ["Yen", "Dollar", "Euro", "Won"]),
    ("What is the boiling point of water?", ["100°C", "90°C", "80°C", "70°C"]),
    ("What is the hardest natural substance on Earth?", ["Diamond", "Gold", "Iron", "Quartz"]),
    ("What is the main ingredient in guacamole?", ["Avocado", "Tomato", "Onion", "Pepper"]),
    ("What is the largest mammal in the world?", ["Blue Whale", "Elephant", "Giraffe", "Shark"]),
    ("What is the capital of Italy?", ["Rome", "Venice", "Florence", "Milan"]),
    ("What is the square root of 16?", ["4", "3", "5", "6"]),
    ("What is the longest river in the world?", ["Nile", "Amazon", "Yangtze", "Mississippi"]),
    ("What is the main language spoken in Brazil?", ["Portuguese", "Spanish", "English", "French"]),
    ("What is the chemical symbol for gold?", ["Au", "Ag", "Fe", "Pb"]),
    ("What is the largest continent?", ["Asia", "Africa", "North America", "Europe"]),
    ("What is the speed of light?", ["299,792 km/s", "150,000 km/s", "300,000 km/s", "400,000 km/s"]),
    ("What is the capital of Canada?", ["Ottawa", "Toronto", "Vancouver", "Montreal"]),
    ("What is the primary ingredient in bread?", ["Flour", "Sugar", "Salt", "Water"]),
    ("What is the tallest mountain in the world?", ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"]),
]
random.shuffle(questions)
score = 0
for question, answers in questions:
    correct_answer = answers[0]
    random_answers = answers[1:]
    random.shuffle(random_answers)
    shuffled_answers = random_answers[:3] + [correct_answer]

    random.shuffle(shuffled_answers)

    print(question)
    for i, answer in enumerate(shuffled_answers):
        print(f"{i + 1}. {answer}")

    user_answer = input("Please select the correct answer: ")

    if user_answer.isdigit() and shuffled_answers[int(user_answer) - 1] == correct_answer:
        print("Correct!\n")
        score += 1
    else:
        print("Incorrect. The correct answer was:", correct_answer, "\n")

print(f"Your final score is: {score}/{len(questions)}")
