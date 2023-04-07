class UserQuiz:
    def __init__(self, id, quiz, user, date_taken=None):
        self.id = id
        self.quiz = quiz
        self.user = user
        self.date_taken = date_taken
        self.answers = []
        self.questions = []
        self.results = []
        self.current = 0
    
    def add_answer(self, answer):
        self.answers.append(answer)

    def add_question(self, question):
        self.questions.append(question)

    def add_results(self, results):
        pass
    