class Quiz:
    def __init__(self, id, title, is_active=False, created_at=None):
        self.id = id
        self.title = title
        self.is_active = is_active
        self.created_at = created_at
        self.questions = []


    def get_number_of_questions(self):
        return len(self.questions)

    

