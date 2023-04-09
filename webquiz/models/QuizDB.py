import mysql.connector
from config import Database
from webquiz.models.Quiz import Quiz
from webquiz.models.Question import Question
from webquiz.models.Choice import Choice
from webquiz.models.Answer import Answer
from webquiz.models.UserQuiz import UserQuiz
from uuid import uuid4

class QuizDB(Database):
    def __init__(self):
        super().__init__()
    
    # CREATE
    def create_quiz(self, title):
        try:
            id = str(uuid4())
            query = """INSERT INTO Quiz (id, title)
                       VALUES (%s, %s)"""
            values = (id, title)
            self.cursor.execute(query, values)
            return id
        
        except mysql.connector.Error as err:
            print(err)

    def create_question(self, category, content, multiple_choice):
        try:
            id = str(uuid4())
            question = Question(id, category, content, multiple_choice)
            query = """INSERT INTO Question (id, category, content, is_multiple_choice)
                       VALUES (%s, %s, %s, %s)"""
            values = (question.id, 
                      question.category,
                      question.content,
                      question.is_multiple_choice)
            self.cursor.execute(query, values)
            return id
        
        except mysql.connector.Error as err:
            print(err)
        
    def create_choice(self, question_id, content, is_correct):
        try:
            id = str(uuid4())
            # choice = Choice(id, question_id, content, is_correct)
            query = """INSERT INTO Choice (id, question, content, is_correct)
                       VALUES (%s, %s, %s, %s)"""
            values = (id, question_id, content, is_correct)
            self.cursor.execute(query, values)
            return id
        
        except mysql.connector.Error as err:
            print(err)

    def create_quiz_question(self, quiz_id, question_id):
        try:
            query = """INSERT INTO QuizQuestion (quiz, question)
                       VALUES (%s, %s)"""
            values = (quiz_id, question_id)
            self.cursor.execute(query, values)

        except mysql.connector.Error as err:
            print(err)

    def create_user_quiz(self, quiz_id, user_id):
        try:
            id = str(uuid4())
            query = """INSERT INTO UserQuiz (id, quiz, user)
                       VALUES (%s, %s, %s)"""
            values = (id, quiz_id, user_id)
            self.cursor.execute(query, values)
            return id
        
        except mysql.connector.Error as err:
            print(err)

    def create_answer(self, user_quiz_id, question_id, content):
        try:
            query = """INSERT INTO Answer (user_quiz, question, content)
                       VALUES (%s, %s, %s)"""
            values = (user_quiz_id, question_id, content)
            self.cursor.execute(query, values)
        
        except mysql.connector.Error as err:
            print(err)
    
    # UPDATE
    def update_quiz(self, id, title):
        try:
            query = """UPDATE Quiz SET title=(%s) WHERE id=(%s)"""
            self.cursor.execute(query, (title, id))
        except mysql.connector.Error as err:
            print(err)

    def update_question(self, id, category, content, is_multiple_choice):
        try:
            query = """UPDATE Question 
                       SET category=(%s), content=(%s), is_multiple_choice=(%s)
                       WHERE id=(%s)"""
            values = (category, content, is_multiple_choice, id)
            self.cursor.execute(query, values)
        except mysql.connector.Error as err:
            print(err)

    def update_answer(self, quiz_id, question_id, new_content):
        try:
            query = """UPDATE Answer SET content=(%s) WHERE user_quiz=(%s) AND question=(%s)"""
            self.cursor.execute(query, (new_content, quiz_id, question_id))
        except mysql.connector.Error as err:
            print(err)

    def update_choice(self, id, content):
        try:
            query = """UPDATE Choice SET content=(%s) WHERE id=(%s)"""
            values = (content, id)
            self.cursor.execute(query, values)

        except mysql.connector.Error as err:
            print(err)

    def update_status(self, quiz_id, status):
        try:
            query = """UPDATE Quiz SET is_active=(%s) WHERE id=(%s)"""
            self.cursor.execute(query, (status, quiz_id,))
        except mysql.connector.Error as err:
            print(err)


    # GET
    def get_quiz(self, id):
        try:
            query = """SELECT * FROM Quiz WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
            quiz = Quiz(*result)
            return quiz
        
        except mysql.connector.Error as err:
            print(err)

    def get_quizzes(self):
        try:
            query = """SELECT * FROM Quiz"""
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            
            quizzes = []
            for quiz in result:
                quizzes.append(Quiz(*quiz))

            return quizzes
        except mysql.connector.Error as err:
            print(err)

    def get_user_quiz(self, id):
        try:
            # query = """SELECT * FROM UserQuiz WHERE id=(%s)"""
            query = """SELECT U.quiz, U.user, U.date_taken, Q.title,
                       SUM(CASE WHEN A.content = (SELECT C.content FROM Choice AS C 
                                                  WHERE C.question = A.question AND C.is_correct=1) 
                                THEN 1 ELSE 0
                            END) AS is_correct
                        FROM UserQuiz AS U
                        INNER JOIN Answer AS A ON A.user_quiz = U.id
                        INNER JOIN Quiz AS Q ON Q.id = U.quiz
                        WHERE U.id=(%s)"""
            
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
            quiz_id, user_id, date_taken, title, correct_answers = result
            user_quiz = UserQuiz(id, quiz_id, user_id, date_taken)
            user_quiz.title = title
            user_quiz.correct = correct_answers
            return user_quiz
        
        except mysql.connector.Error as err:
            print(err)

    def get_user_quizzes(self, user_id):
        try:
            query = """SELECT U.id, U.quiz, U.date_taken, Q.title,
                       SUM(CASE WHEN A.content = (SELECT C.content FROM Choice AS C 
                                                  WHERE C.question = A.question AND C.is_correct=1) 
                                THEN 1 ELSE 0
                            END) AS is_correct
                        FROM UserQuiz AS U
                        INNER JOIN Answer AS A ON A.user_quiz = U.id
                        INNER JOIN Quiz AS Q ON Q.id = U.quiz
                        WHERE U.user=(%s)
                        GROUP BY U.id
                        ORDER BY U.date_taken DESC"""
        
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchall()
            quizzes = []
            for quiz in result:
                id, quiz_id, date_taken, title, correct_answers = quiz
                user_quiz = UserQuiz(id, quiz_id, user_id, date_taken)
                user_quiz.title = title
                user_quiz.correct = correct_answers
                quizzes.append(user_quiz)

            return quizzes
        except mysql.connector.Error as err:
            print(err)

    def get_quiz_attempts(self, quiz_id, user_id):
        try:
            query = """SELECT COUNT(*) FROM UserQuiz WHERE quiz=(%s) AND user=(%s)"""
            self.cursor.execute(query, (quiz_id, user_id))
            result = self.cursor.fetchone()
            return result[0]
        except mysql.connector.Error as err:
            print(err)

    def get_question(self, id):
        try:
            query = """SELECT * FROM Question WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
            question = Question(*result)
            return question
        
        except mysql.connector.Error as err:
            print(err)

    def get_all_questions(self):
        try:
            query = """SELECT * FROM Question"""
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            questions = []
            for q in result:
                questions.append(Question(*q))

            return questions

        except mysql.connector.Error as err:
            print(err)

    # def get_questions_by_category(self, category):
    #     try:
    #         query = """SELECT * FROM Question WHERE category=(%s)"""
    #         self.cursor.execute(query, (category,))
    #         result = self.cursor.fetchall()
    #         questions = []
    #         for q in result:
    #             questions.append(Question(*q))

    #         return questions

    #     except mysql.connector.Error as err:
    #         print(err)

    def get_questions(self, quiz):
        try:
            query = """SELECT Q.id, Q.category, Q.content, Q.is_multiple_choice
                       FROM Question AS Q
                       INNER JOIN QuizQuestion AS QQ ON QQ.question = Q.id 
                       WHERE QQ.quiz=(%s)"""
            self.cursor.execute(query, (quiz.id,))
            result = self.cursor.fetchall()

            for question in result:
                quiz.add_question(Question(*question))

        except mysql.connector.Error as err:
            print(err)

    def get_questions_v2(self, quiz_id):
        try:
            query = """SELECT Q.id, Q.category, Q.content, Q.is_multiple_choice
                       FROM Question AS Q
                       INNER JOIN QuizQuestion AS QQ ON QQ.question = Q.id 
                       WHERE QQ.quiz=(%s)"""
            self.cursor.execute(query, (quiz_id,))
            result = self.cursor.fetchall()
            questions = []
            for question in result:
                questions.append(Question(*question))

            return questions

        except mysql.connector.Error as err:
            print(err)

    def get_categories(self):
        try:
            self.cursor.execute("SELECT * FROM Category ORDER BY name DESC")
            result = self.cursor.fetchall()
            return result
        
        except mysql.connector.Error as err:
            print(err)

    def get_choice(self, id):
        try:
            query = """SELECT * FROM Choice WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
            choice = Choice(*result)
            return choice
        
        except mysql.connector.Error as err:
            print(err)

    def get_choices(self, question_id):
        try:
            query = """SELECT * FROM Choice WHERE question=(%s)"""
            self.cursor.execute(query, (question_id,))
            result = self.cursor.fetchall()
            choices = []
            for choice in result:
                choices.append(Choice(*choice))
            
            return choices

        except mysql.connector.Error as err:
            print(err)

    def get_alternatives(self, question_id):
        try:
            query = """SELECT * FROM Choice 
                       WHERE question=(%s) AND NOT is_correct"""
            self.cursor.execute(query, (question_id,))
            result = self.cursor.fetchall()
            choices = []        
            for choice in result:
                choices.append(Choice(*choice))

            return choices
        except mysql.connector.Error as err:
            print(err)

    def get_answer(self, question_id):
        try:
            query = """SELECT * FROM Choice WHERE question=(%s) AND is_correct=1"""
            self.cursor.execute(query, (question_id,))
            result = self.cursor.fetchone()
            answer = Choice(*result)
            return answer
        except mysql.connector.Error as err:
            print(err)
    
    def get_user_answer(self, quiz_id, question_id):
        try:
            query = """SELECT content FROM Answer WHERE user_quiz=(%s) AND question=(%s)"""
            self.cursor.execute(query, (quiz_id, question_id))
            result = self.cursor.fetchone()
            answer = Answer(quiz_id, question_id, content=result[0])
            return answer
        except mysql.connector.Error as err:
            print(err)

    def get_user_answers(self, question):
        try:
            query = """SELECT A.user_quiz, content FROM Answer AS A
                       INNER JOIN UserQuiz ON UserQuiz.id = A.user_quiz 
                       WHERE question=(%s)"""
            self.cursor.execute(query, (question.id,))
            result = self.cursor.fetchall()
            for answer in result:
                user_quiz, content = answer
                user_answer = Answer(user_quiz, question.id, content)
                question.add_user_answer(user_answer)

        except mysql.connector.Error as err:
            print(err)

    def get_user_answers_by_user_quiz(self, user_quiz_id):
        try:
            query = """SELECT * FROM Answer WHERE user_quiz=(%s)"""
            self.cursor.execute(query, (user_quiz_id,))
            result = self.cursor.fetchall()
            answers = []
            for answer in result:
                answers.append(Answer(*answer))

            return answers
        except mysql.connector.Error as err:
            print(err)


    def search_questions(self, category, search_text):
        try:
            if category and search_text:
                search_text = '%' + search_text + '%'
                query = """SELECT * FROM Question WHERE content LIKE (%s) AND category=(%s)"""
                self.cursor.execute(query, (search_text, category))
            elif category:
                query = """SELECT * FROM Question WHERE category=(%s)"""
                self.cursor.execute(query, (category,))
            elif search_text:
                search_text = '%' + search_text + '%'
                query = """SELECT * FROM Question WHERE content LIKE (%s)"""
                self.cursor.execute(query, (search_text,))
            else:
                query = """SELECT * FROM Question"""
                self.cursor.execute(query)

            result = self.cursor.fetchall()
            questions = []
            for q in result:
                questions.append(Question(*q))
            return questions
        except mysql.connector.Error as err:
            print(err)

    # DELETE
    def delete_quiz(self, id):
        try:
            query = """DELETE FROM Quiz WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
        except mysql.connector.Error as err:
            print(err)

    def delete_question(self, id):
        try:
            query = """DELETE FROM Question
                    WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
        except mysql.connector.Error as err:
            print(err)

    def delete_choice(self, id):
        try:
            query = """DELETE FROM Choice
                       WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
        except mysql.connector.Error as err:
            print(err)
    
    def get_answers_with_result(self, user_quiz_id):
        try:
            query = """SELECT Q.id, Q.content, A.content,
                       (SELECT C.content FROM Choice AS C WHERE C.question = A.question AND C.is_correct=1)
                        FROM Answer AS A INNER JOIN Question AS Q ON Q.id = A.question
                        WHERE A.user_quiz=(%s)"""
            
            self.cursor.execute(query, (user_quiz_id,))
            result = self.cursor.fetchall()
            answers = []
            
            for item in result:
                question_id, question, user_answer, correct_answer = item
                answer = Answer(user_quiz_id, question_id, user_answer)
                answer.question_content = question

                if user_answer == correct_answer:
                    answer.is_correct = True

                answers.append(answer)

            return answers   

        except mysql.connector.Error as err:
            print(err)
