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
        self.score = 0

    def calculate_score(self):
        correct = len([a for a in self.answers if a.is_correct])
        self.score = round((correct * 100) / len(self.answers))


    
