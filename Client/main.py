import sys
from PySide6.QtWidgets import QApplication

from models.user_model import UserModel
from models.portfolio_model import PortfolioModel
from models.stock_model import StockModel

from views.auth_views import AuthStackedWidget
from views.main_view import MainWindow
from views.portfolio_view import PortfolioView
from views.stock_view import StockView

from presenters.auth_presenter import AuthPresenter
from presenters.main_presenter import MainPresenter
from presenters.portfolio_presenter import PortfolioPresenter
from presenters.stock_presenter import StockPresenter

from services.api_service import ApiService


def main():
    # Create application
    app = QApplication(sys.argv)
    
    # Create API service
    api_service = ApiService()
    
    # Create models
    user_model = UserModel()
    portfolio_model = PortfolioModel()
    stock_model = StockModel()
    
    # Create main window and views
    main_window = MainWindow()
    auth_view = AuthStackedWidget()
    portfolio_view = PortfolioView()
    stock_view = StockView()
    
    # Set up views in main window
    main_window.set_auth_widget(auth_view)
    main_window.set_portfolio_widget(portfolio_view)
    main_window.set_stocks_widget(stock_view)
    
    # Create presenters
    auth_presenter = AuthPresenter(auth_view, main_window, user_model, api_service)
    main_presenter = MainPresenter(main_window, user_model)
    portfolio_presenter = PortfolioPresenter(portfolio_view, user_model, portfolio_model, api_service)
    stock_presenter = StockPresenter(stock_view, user_model, stock_model, api_service)
    
    # Initialize application
    main_presenter.initialize_app()
    
    # Show main window in full screen
    main_window.showMaximized()
    
    # Start application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()