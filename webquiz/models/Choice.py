class Choice():
    def __init__(self, id, question, content, is_correct):
        self.id = id
        self.question = question
        self.content = content
        self.is_correct = int(is_correct)