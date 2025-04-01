from controllers.DbController import DbController


class WindowManager:
    _instance = None
    def new(cls, *args, **kwargs): # реализация синглтона для единого управления окнами
        if not cls._instance:
            cls._instance = super(WindowManager, cls).new(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        if not hasattr(self, 'windows'):
            self.windows = {}

        self.current_user = {} # единая точка хранения текущего пользователя
        self.db_controller = DbController() # единый доступ к БД

    def register_window(self, name, window): # регистрирует окно по имени
        self.windows[name] = window

    def get_window(self, name): # вернуть окно по имени
        return self.windows[name]

    def show_window(self, name_to_open, name_to_close): # показать окно
        window = self.get_window(name_to_open)
        window_to_close = self.get_window(name_to_close)
        if window:
            window.show()
            if window_to_close:
                window_to_close.close()
        else:
            print(f"Окно {name_to_open} не найдено")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from windows.MainWindow import MainWindow
    from HomeWindow import HomeWindow
    from ExamWindow import ExamWindow

    app = QApplication(sys.argv)

    manager = WindowManager()
    main_window = MainWindow(manager)
    home_window = HomeWindow(manager)
    exam_window = ExamWindow(manager)

    manager.register_window('main', main_window)
    manager.register_window('home', home_window)
    manager.register_window('exam', exam_window)

    main_window.show() # показать окно логина

    sys.exit(app.exec())