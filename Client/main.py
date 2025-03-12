import sys
from PySide6.QtWidgets import QApplication
from views.main_view import MainWindow
from presenters.main_presenter import MainPresenter
from models.user_model import UserModel
from services.session_service import SessionService
from services.api_service import ApiService

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Stock Portfolio Manager")
    
    # Initialize services
    api_service = ApiService()
    session_service = SessionService()
    
    # Initialize model
    user_model = UserModel()
    
    # Initialize main window (view)
    main_window = MainWindow()
    
    # Initialize presenter and connect it to view and model
    presenter = MainPresenter(main_window, user_model, api_service, session_service)
    
    # Show the main window in fullscreen mode
    main_window.showMaximized()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()