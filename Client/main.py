from PySide6.QtWidgets import QApplication, QStackedWidget

from Views.loginView import LoginWindow
# from Views.portfolioView import PortfolioWindow
from Views.mainView import MainView

from Models.loginModel import LoginModel
# from Models.portfolioModel import PortfolioModel
from Models.mainModel import MainModel

from Presenters.loginPresenter import LoginPresenter
# from Presenters.portfolioPresenter import PortfolioPresenter
from Presenters.mainPresenter import MainPresenter

import sys


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Stock Portfolio Manager")

        # Initialize stacked widget
        self.stack = QStackedWidget()

        # Initialize views
        self.login_window = LoginWindow()
        self.main_window = MainView()

        # Add views to the stack
        self.stack.addWidget(self.login_window)
        self.stack.addWidget(self.main_window)

        # Initialize models
        login_model = LoginModel()
        main_model = MainModel()

        # Link presenters
        self.login_window.presenter = LoginPresenter(
            self,
            self.login_window,
            login_model
        )

        # Set main window presenter
        self.main_window.presenter = MainPresenter(
            main_model,
            self.main_window
        )

        # Start with login view
        self.stack.setCurrentWidget(self.login_window)
        self.stack.resize(800, 600)
        self.stack.show()

    def switch_to_dashboard(self, user_id):
        """Switch to the main dashboard view."""
        # You could pass user_id to MainModel if needed
        self.stack.setCurrentWidget(self.main_window)

    def run(self):
        sys.exit(self.app.exec())


def main():
    controller = AppController()
    controller.run()


if __name__ == "__main__":
    main()
