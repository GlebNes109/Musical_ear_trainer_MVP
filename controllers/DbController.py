import sqlite3
import time
from readline import get_current_history_length


# Класс для работы с БД
class DbController():

    EXAM_PASSED_CONSTANT = "passed"
    EXAM_FAILED_CONSTANT = "failed"

    def __init__(self):
        self.dbstring = "db/MusicalTrainer.sqlite"

    # сохранить попытку экзамена
    def save_test_attempt(self, test_attempt):
        current_date = int(time.time())
        connection = sqlite3.connect(self.dbstring)

        cursor = connection.cursor()
        print(test_attempt.user_id, current_date, test_attempt.result)
        query = """INSERT INTO TestAttempts (user_id, created_date, result) VALUES (?, ?, ?)"""
        cursor.execute(query, (test_attempt.user_id, current_date, test_attempt.result,))
        test_attempt.id = cursor.lastrowid # считать ID только что вставленной попытки

        connection.commit()
        connection.close()

        self.save_answers(test_attempt) # сохранить ответы этого экзамена

    # сохранить ответы одной попытки экзамена
    def save_answers(self, test_attempt):
        connection = sqlite3.connect(self.dbstring)
        cursor = connection.cursor()

        for a in test_attempt.answers:
            query = """INSERT INTO TestAnswers (attempt_id, correct_answer, given_answer, is_correct) VALUES (?, ?, ?, ?)"""
            cursor.execute(query, (test_attempt.id, a.correct_answer, a.given_answer, a.is_correct,))

        connection.commit()
        connection.close()

    # добавить нового пользователя
    def add_user(self, login, password_hash):
        connection = sqlite3.connect(self.dbstring)
        cursor = connection.cursor()

        query = """INSERT INTO Users (login, password_hash) VALUES (?, ?)"""
        cursor.execute(query, (login, password_hash,))

        connection.commit()
        connection.close()

    # аутентификация пользователя
    def auth_user(self, login, password_hash):
        connection = sqlite3.connect(self.dbstring)
        cursor = connection.cursor()

        result = cursor.execute("""select id from users where login = ? and password_hash = ?""", (login, password_hash)).fetchall()
        connection.close()

        if result:
            return result[0][0]
        else:
            return None

    def get_total_tries(self, user_id):
        connection = sqlite3.connect(self.dbstring)
        cursor = connection.cursor()

        result = cursor.execute("""select count(*) from TestAttempts where user_id = ?""",
                                (user_id,)).fetchall()
        connection.close()

        if result:
            return int(result[0][0])
        else:
            return 0

    def get_success_tries(self, user_id):
        connection = sqlite3.connect(self.dbstring)
        cursor = connection.cursor()

        result = cursor.execute("""select count(*) from TestAttempts where user_id = ? and result = ?""",
                                (user_id,DbController.EXAM_PASSED_CONSTANT,)).fetchall()
        connection.close()

        if result:
            return int(result[0][0])
        else:
            return 0

    def get_answers_cnt(self, user_id, get_correct=1):
        connection = sqlite3.connect(self.dbstring)
        cursor = connection.cursor()

        result = cursor.execute("""select count(*) from testattempts at join testanswers an on at.id = an.attempt_id where at.user_id = ? and an.is_correct = ?""",
                                (user_id,get_correct)).fetchall()
        connection.close()

        if result:
            return int(result[0][0])
        else:
            return 0

    def save_avatar(self, user_id, file_binary_data):
        connection = sqlite3.connect(self.dbstring)
        cursor = connection.cursor()

        cursor.execute("""UPDATE users SET image = ? WHERE id = ?;""", (file_binary_data, user_id))

        connection.commit()
        connection.close()

    def get_avatar(self, user_id):
        connection = sqlite3.connect(self.dbstring)
        cursor = connection.cursor()

        avatar_data = cursor.execute("""SELECT image FROM users WHERE id = ?;""", (user_id, )).fetchone()

        connection.commit()
        connection.close()

        if avatar_data and avatar_data[0]:  # Если аватар есть
            return avatar_data[0]
        else:
            return None  # Если аватар отсутствует