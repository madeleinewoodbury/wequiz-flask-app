class Answer:
    def __init__(self, user_quiz, question, content):
        self.user_quiz = user_quiz
        self.question = question
        self.content = content
        self.question_content = None
        self.is_correct = False