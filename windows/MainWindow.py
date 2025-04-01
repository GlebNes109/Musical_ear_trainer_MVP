import hashlib
from PyQt6.QtWidgets import QMainWindow, QLineEdit

from Models.User import User
from windows.pages.mainpage import Ui_Dialog

# вычислить хеш строки
def calculate_hash(str_to_encode):
    sha256hash = hashlib.sha256()
    sha256hash.update(str_to_encode.encode('utf-8'))
    return sha256hash.hexdigest()

class MainWindow(QMainWindow, Ui_Dialog):
    def __init__(self, manager):
        super().__init__()
        self.setupUi(self)
        self.manager = manager
        self.setWindowTitle("Главное окно")
        self.resize(653, 242)
        self.registration_button.clicked.connect(self.reg_click)
        self.login_button.clicked.connect(self.login_click)
        self.statusBar().showMessage("")
        self.login_name.setPlaceholderText("Ваш логин")
        self.login_password.setPlaceholderText("Ваш пароль")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.registration_password.setPlaceholderText("Придумайте пароль")
        self.registration_retype_password.setPlaceholderText("Повторите пароль")
        self.registration_name.setPlaceholderText("Придумайте логин")
        self.registration_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.registration_retype_password.setEchoMode(QLineEdit.EchoMode.Password)

    # аутентификация существующего пользователя
    def login_click(self):
        self.statusBar().showMessage("")
        name = self.login_name.text()
        password = self.login_password.text()
        user_id = self.manager.db_controller.auth_user(name, calculate_hash(password))  # проверка есть ли такой пользователь в базе

        if user_id:
            print(user_id, name)
            self.manager.current_user = User(user_id, name)
            print(self.manager.current_user.name)
            self.login_name.setText("")
            self.login_password.setText("")
            self.manager.show_window("home", "main")
            # self.statusBar().showMessage("Успешный вход")
        else:
            self.statusBar().showMessage("Неверный логин или пароль")

    # регистрация нового пользователя
    def reg_click(self):
        self.statusBar().showMessage("")
        if self.registration_password.text() == self.registration_retype_password.text():
            name = self.registration_name.text()
            passwd = self.registration_password.text()
            if any(char.isdigit() for char in passwd):
                self.manager.db_controller.add_user(name, calculate_hash(passwd))  # регистрация пользователя
                self.statusBar().showMessage(f"Пользователь {name} добавлен, войдите в систему")
            else:
                self.statusBar().showMessage("Пароль должен содержать хотя бы 1 цифру")
        else:
            self.statusBar().showMessage("Пароли не совпадают")