class UserQuiz:
    def __init__(self, id, quiz, user, date_taken=None):
        self.id = id
        self.quiz = quiz
        self.user = user
        self.date_taken = date_taken
        self.title = None
        self.answers = []
        self.questions = []
        self.results = []
        self.correct = 0
        self.score = 0
    
    def add_answer(self, answer):
        self.answers.append(answer)

    def add_question(self, question):
        self.questions.append(question)

    def calculate_score(self):
        self.score = round((self.correct * 100) / len(self.questions))

    def add_results(self, results):
        pass
    