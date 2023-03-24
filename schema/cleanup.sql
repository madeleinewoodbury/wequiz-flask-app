DELETE FROM QuizQuestion;
DELETE FROM Choice;
DELETE FROM Question;
DELETE FROM Quiz;
DELETE FROM User 
WHERE email not in('jdoe@email.com', 'kari@email.com');