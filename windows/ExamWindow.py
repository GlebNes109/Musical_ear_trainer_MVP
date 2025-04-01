from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem

from controllers.AudioController import AudioController
from controllers.DbController import DbController
from PyQt6.QtCore import QTimer
from Models.TestAttempt import TestAttempt
from Models.TestAttemptAnswer import TestAttemptAnswer
# from Models.TestAttemptAnswer import TestAttemptAnswer
from windows.pages.exampage import Ui_Dialog
# from test import passwd
import random


class ExamWindow(QMainWindow, Ui_Dialog):
    def __init__(self, manager):
        super().__init__()
        self.setupUi(self)
        self.manager = manager
        self.rounds_count = 3 # количество упражнений в экзамене
        self.audio_controller = AudioController()
        self.current_round = 0
        self.setWindowTitle("Страница экзамена")
        self.finish_button.clicked.connect(self.finish_exam)
        self.start_button.clicked.connect(self.start_exam)
        self.next_button.clicked.connect(self.next_question)
        self.do_button.clicked.connect(lambda: self.push_note_button("до"))
        self.re_button.clicked.connect(lambda: self.push_note_button("ре"))
        self.mi_button.clicked.connect(lambda: self.push_note_button("ми"))
        self.fa_button.clicked.connect(lambda: self.push_note_button("фа"))
        self.sol_button.clicked.connect(lambda: self.push_note_button("соль"))
        self.la_button.clicked.connect(lambda: self.push_note_button("ля"))
        self.si_button.clicked.connect(lambda: self.push_note_button("си"))
        # self.statusBar().showMessage("")

    def push_note_button(self, note_name):
        self.result_table.setItem(0, self.current_round, QTableWidgetItem(note_name))

    def showEvent(self, event):
        self.statusBar().showMessage("")
        self.generate_exam()
        self.do_button.setEnabled(False)
        self.re_button.setEnabled(False)
        self.mi_button.setEnabled(False)
        self.fa_button.setEnabled(False)
        self.sol_button.setEnabled(False)
        self.la_button.setEnabled(False)
        self.si_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.finish_button.setEnabled(False)
        self.start_button.setEnabled(True)


    # начать экзамен
    def start_exam(self):
        # разблокировать кнопки нот

        # сыграть настройку
        self.audio_controller.play_tuning()
        self.do_button.setEnabled(True)
        self.re_button.setEnabled(True)
        self.mi_button.setEnabled(True)
        self.fa_button.setEnabled(True)
        self.sol_button.setEnabled(True)
        self.la_button.setEnabled(True)
        self.si_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self.next_button.setEnabled(True)
        self.finish_button.setEnabled(True)
        # сыграть первую ноту из загаданных нот
        self.current_round = 0
        note_to_play = self.exam["questions"][self.current_round]["answer"]
        self.audio_controller.play_note(note_to_play)
        self.label_info.setText(f"Вопрос: {self.current_round + 1}/{self.rounds_count}")

    # сыграть следующую загаданную ноту
    def next_question(self):
        self.current_round += 1
        if self.current_round == self.rounds_count:
            self.current_round = 0
        self.label_info.setText(f"Вопрос: {self.current_round + 1}/{self.rounds_count}")
        note_to_play = self.exam["questions"][self.current_round]["answer"]
        self.audio_controller.play_note(note_to_play)

    # сгенерировать вопросы для экзамена
    def generate_exam(self):
        variants = ["до", "ре", "ми", "фа", "соль", "ля", "си"] # варианты заданий
        self.exam = {"questions": []}

        self.result_table.setRowCount(1)
        self.result_table.setColumnCount(self.rounds_count)

        for c in range(self.rounds_count):
            q = {"number": c + 1, "answer": random.choice(variants)}
            print(q)
            self.exam["questions"].append(q)
            self.result_table.setItem(0, c, QTableWidgetItem(""))


    # завершить экзамен
    def finish_exam(self):
        att = TestAttempt() # создать объект попытки сдачи экзамена
        att.user_id = self.manager.current_user.id
        correct_answers_cnt = 0
        # проверить что сдал экзамен
        passed = True
        for cell in range(self.rounds_count): # считать из tableWidget в
            user_answer = self.result_table.item(0, cell).text()
            correctanswer = self.exam["questions"][cell]["answer"] # взять верный ответ
            print(user_answer, correctanswer)

            if user_answer != correctanswer:
                passed = False
            else:
                correct_answers_cnt += 1

            testAttemptAnswer = TestAttemptAnswer(att.user_id, (cell + 1), correctanswer, user_answer, int(passed))
            att.answers.append(testAttemptAnswer)

        if not passed:
            res = "провален"
            # print("не прошел экзамен")
            att.result = DbController.EXAM_FAILED_CONSTANT
        else:
            res = "сдан"
            # print("прошел экзамен")
            att.result = DbController.EXAM_PASSED_CONSTANT

        self.manager.db_controller.save_test_attempt(att)  # сохранить ответы попытки
        self.statusBar().showMessage(f"тест {res}, правильных ответов {correct_answers_cnt}, всего {len(att.answers)}") # результаты теста в статусбаре
        QTimer.singleShot(5000, lambda: self.manager.show_window("home", "exam"))


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ExamWindow()
#     window.show()
#     sys.exit(app.exec())