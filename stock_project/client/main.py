from PySide6.QtWidgets import QApplication, QStackedWidget
from Views.loginView import LoginWindow
from Views.portfolioView import PortfolioWindow
from Models.loginModel import LoginModel
from Models.portfolioModel import PortfolioModel
from Presenters.loginPresenter import LoginPresenter
from Presenters.portfolioPresenter import PortfolioPresenter


class AppController:
    def __init__(self):
        self.app = QApplication([])
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

        portfolioModel = PortfolioModel()
        self.portfolio_window.presenter = PortfolioPresenter(self, portfolioModel, self.portfolio_window)

        # Start with the login view
        self.stack.setCurrentWidget(self.login_window)
        self.stack.show()

    def switch_to_dashboard(self):
        """Switch to the dashboard view."""
        self.stack.setCurrentWidget(self.portfolio_window)

    def run(self):
        self.app.exec()


def main():
    controller = AppController()
    controller.run()


if __name__ == "__main__":
    main()