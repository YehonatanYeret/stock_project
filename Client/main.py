
from PySide6.QtWidgets import QApplication, QStackedWidget
from Views.loginView import LoginWindow
from Views.portfolioView import PortfolioWindow

from Views.mainView import MainView
from Models.loginModel import LoginModel
from Models.portfolioModel import PortfolioModel
from Models.mainModel import MainModel
from Presenters.loginPresenter import LoginPresenter
from Presenters.portfolioPresenter import PortfolioPresenter

from Presenters.mainPresenter import MainPresenter
import sys

"""
class AppController:
    def __init__(self):
        self.app = QApplication([])
        self.app.setApplicationName("Yehonatan HaGever")

        self.stack = QStackedWidget()

        # Initialize views
        self.login_window = LoginWindow()
        self.portfolio_window = PortfolioWindow()

        # Add views to the stack
        self.stack.addWidget(self.login_window)
        self.stack.addWidget(self.portfolio_window)

        # Link presenter to the login view
        login_model = LoginModel()
        self.login_window.presenter = LoginPresenter(self, self.login_window, login_model)

        # Start with the login view
        self.stack.setCurrentWidget(self.login_window)
        self.stack.show()

    def switch_to_dashboard(self, user_id):
        # Switch to the dashboard view.
        
        self.portfolioModel = PortfolioModel(user_id)
        self.portfolio_window.presenter = PortfolioPresenter(self, self.portfolioModel, self.portfolio_window)
        self.stack.setCurrentWidget(self.portfolio_window)

    def run(self):
        self.app.exec()


def main():
    controller = AppController()
    controller.run()


if __name__ == "__main__":
    main()
"""


"""
# File: app_controller.py
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget

from views.login_view import LoginWindow
from views.main_view import MainView  # Reusing the previous multi-page view
from models.login_model import LoginModel
from models.main_model import MainModel
from presenters.login_presenter import LoginPresenter
from presenters.main_presenter import MainPresenter"""

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Stock Portfolio Manager")
        
        # Global dark stylesheet
     
        
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