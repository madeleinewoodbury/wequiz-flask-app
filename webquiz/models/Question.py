class Question:
    def __init__(self, id, category, content, is_multiple_choice):
        self.id = id
        self.category = category
        self.content = content
        self.answer = None
        self.is_multiple_choice = is_multiple_choice
        self.choices = []
        self.quiz = None
        self.user_answers = []
        self.quizzes = []

    def add_choice(self, choice):
        self.choices.append(choice)

    def add_user_answer(self, answer):
        self.user_answers.append(answer)


