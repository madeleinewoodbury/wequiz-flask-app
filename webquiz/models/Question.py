from config import Database
import mysql.connector

class Choice():
    def __init__(self, id, question, content, is_correct):
        self.id = id
        self.question = question
        self.content = content
        self.is_correct = int(is_correct)

class Question:
    def __init__(self, id, category, content, is_multiple_choice):
        self.id = id
        self.category = category
        self.content = content
        self.answer = None
        self.is_multiple_choice = is_multiple_choice
        self.choices = []
        self.quiz = None

    def add_choice(self, id, content):
        self.choices.append(Choice(id, self.id, content, False))


class QuestionTable(Database):
    def __init__(self):
        super().__init__()
    
    def create(self, question):
        query = """INSERT INTO Question (id, category, content, is_multiple_choice)
                    VALUES (%s, %s, %s, %s)"""
        values = (question.id, 
                  question.category,
                  question.content,
                  question.is_multiple_choice)
        
        self.cursor.execute(query, values)

        if question.quiz:
            self.create_quizQuestion(quiz_id=question.quiz, question_id=question.id)

        # add answer
        self.create_choice(question.answer)

        # add alternatives
        if question.choices:
            for choice in question.choices:
                self.create_choice(choice)
    
    def create_choice(self, choice):
        query = """INSERT INTO Choice (id, question, content, is_correct)
                    VALUES (%s, %s, %s, %s)"""
        values = (choice.id, 
                  choice.question, 
                  choice.content, 
                  choice.is_correct)
        
        self.cursor.execute(query, values)

    def update(self, question):
        id = question.id
        category = question.category
        content = question.content
        is_multiple_choice = question.is_multiple_choice

        query = """UPDATE Question 
                    SET category=(%s), content=(%s), is_multiple_choice=(%s)
                    WHERE id=(%s)"""
        values = (category, content, is_multiple_choice, id)
        self.cursor.execute(query, values)

    def update_choice(self, choice):
        query = """UPDATE Choice SET content=(%s) WHERE id=(%s)"""
        values = (choice.content, choice.id)
        self.cursor.execute(query, values)

    def create_quizQuestion(self, quiz_id, question_id):
        query = """INSERT INTO QuizQuestion (quiz, question)
                    VALUES (%s, %s)"""
        values = (quiz_id, question_id)

        self.cursor.execute(query, values)

    def get_question(self, id):
        query = """SELECT * FROM Question WHERE id=(%s)"""
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        question = Question(*result)
        
        return question

    def get_answer(self, question_id):
        query = """SELECT * FROM Choice WHERE question=(%s) AND is_correct=1"""
        self.cursor.execute(query, (question_id,))
        result = self.cursor.fetchone()
        answer = Choice(*result)
        return answer
    
    def get_choices(self, question_id):
        query = """SELECT * FROM Choice WHERE question=(%s)"""
        self.cursor.execute(query, (question_id,))
        result = self.cursor.fetchall()
        choices = []

        for choice in result:
            choices.append(Choice(*choice))
        return choices
    
    def get_alternatives(self, id):
        query = """SELECT * FROM Choice 
                WHERE question=(%s) AND NOT is_correct"""
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchall()
        
        choices = []        
        for choice in result:
            choices.append(Choice(*choice))

        return choices

    def delete(self, id):
        query = """DELETE FROM Question
                WHERE id=(%s)"""
        self.cursor.execute(query, (id,))
    
    def delete_choice(self, id):
        query = """DELETE FROM Choice
                WHERE id=(%s)"""
        self.cursor.execute(query, (id,))

    def delete_alternatives(self, id):
        alternatives = self.get_alternatives(id)
        if alternatives:
            for choice in alternatives:
                self.delete_choice(choice.id)