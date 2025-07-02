import random

class Questions:
    def __init__(self, filename):
        self.filename = filename
        self.questions = []
        self._load_questions()

    def _load_questions(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            blocks = content.split('\n\n')
            for block in blocks:
                lines = block.strip().split('\n')
                if len(lines) >= 2:
                    question = lines[0].strip()
                    answers = [line.strip() for line in lines[1:] if line.strip()]
                    if len(answers) >= 2:
                        self.questions.append((question, answers))

    def shuffle(self):
        random.shuffle(self.questions)

    def get_shuffled_answers(self, correct_answer, wrong_answers):
        sample_size = min(3, len(wrong_answers))
        options = random.sample(wrong_answers, sample_size) + [correct_answer]
        random.shuffle(options)
        return options

    def add_question(self, question, answers):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(f"{question}\n" + "\n".join(answers) + "\n\n")
        self.questions.append((question, answers))
        print("Question added successfully!")
