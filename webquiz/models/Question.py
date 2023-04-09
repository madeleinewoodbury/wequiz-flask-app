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



