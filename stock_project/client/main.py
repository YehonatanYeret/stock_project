from PySide6.QtWidgets import QApplication

from Views.loginView import *
from Presenters.loginPresenter import *


def main():
    app = QApplication([])
    login_window = LoginWindow()
    login_model = LoginModel()
    login_window.show() 
    login_window.presenter = LoginPresenter(login_window, login_model)
    app.exec()

if __name__ == "__main__":
    main()