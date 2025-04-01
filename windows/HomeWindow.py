from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtCore import Qt, QByteArray

from windows.pages.homepage import Ui_Dialog


class HomeWindow(QMainWindow, Ui_Dialog):

    DEFAULT_FILENAME_CONSTANT = 'img/default_image.png' # путь к аватарке по умолчанию

    def __init__(self, manager):
        super().__init__()
        self.setupUi(self)
        self.manager = manager
        self.training_button.hide()
        self.setWindowTitle("Домашняя страница")

        self.exit_button.clicked.connect(self.logout)
        self.exam_button.clicked.connect(self.start_exam)
        self.upload_button.clicked.connect(self.upload_avatar)

    def showEvent(self, event):
        self.hello_name_label.setText(f"Здравствуйте, {self.manager.current_user.name}") # вывести логин текущего юзера
        self.load_statistics() # подтянуть статистику экзаменов
        self.load_avatar() # загрузить аватарку

        super().showEvent(event)

    def load_statistics(self):
        user_id = self.manager.current_user.id

        # достать статистику из бд
        total_tries = self.manager.db_controller.get_total_tries(user_id)
        success_tries = self.manager.db_controller.get_success_tries(user_id)
        correct_cnt = self.manager.db_controller.get_answers_cnt(user_id)
        incorrect_cnt = self.manager.db_controller.get_answers_cnt(user_id, 0)

        # обновить на форме
        self.num_total_tries.display(total_tries)
        self.num_success_tries.display(success_tries)
        self.num_correct_cnt.display(correct_cnt)
        self.num_incorrect_cnt.display(incorrect_cnt)

    # загрузить новый аватар
    def upload_avatar(self):
        file_path = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0] # выбрать файл на диске
        with open(file_path, 'rb') as file: # считать из файла
            file_data = file.read()

        # сохранить в бд
        user_id = self.manager.current_user.id
        self.manager.db_controller.save_avatar(user_id, file_data)

        # установить на виджет
        self.load_avatar_to_widget(file_data)

    # подтянуть аватар пользователя
    def load_avatar(self):
        avatar_data = self.manager.db_controller.get_avatar(self.manager.current_user.id)

        if avatar_data:
            self.load_avatar_to_widget(avatar_data)
        else: # картинка по умолчанию
            self.load_avatar_to_widget(None, 1)

    # установить аватар из бинарных данных
    def load_avatar_to_widget(self, file_binary_data, set_default=0):
        pixmap = QPixmap()

        if set_default == 1:
            pixmap = QPixmap(HomeWindow.DEFAULT_FILENAME_CONSTANT) # картинка по умолчанию
        else:
            pixmap.loadFromData(QByteArray(file_binary_data))  # загрузка аватара из байтов

        scaled_pixmap = pixmap.scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setPixmap(scaled_pixmap)

    def logout(self):
        self.manager.show_window("main", "home") # вернуться на экран логина

    def start_exam(self):
        self.manager.show_window("exam", "home") # перейти на экран экзамена




