class MainPresenter:
    """
    Main presenter that coordinates the overall application flow
    """
    def __init__(self, main_window, user_model):
        """
        Initialize the main presenter
        
        Args:
            main_window: The main application window
            user_model: The user model to track authentication status
        """
        self.view = main_window
        self.user_model = user_model
        
        # Register as observer to receive updates from user model
        self.user_model.register_observer(self)
        
        # Connect signals from main window
        self.connect_signals()
    
    def connect_signals(self):
        """Connect signals from the main window to handler methods"""
        # Authentication signals
        self.view.login_requested.connect(self.handle_login)
        self.view.register_requested.connect(self.handle_register)
        self.view.logout_requested.connect(self.handle_logout)
        
        # Navigation signals
        self.view.dashboard_requested.connect(lambda: self.handle_navigation("dashboard"))
        self.view.portfolio_requested.connect(lambda: self.handle_navigation("portfolio"))
        self.view.stocks_requested.connect(lambda: self.handle_navigation("stocks"))
        self.view.transactions_requested.connect(lambda: self.handle_navigation("transactions"))
        self.view.settings_requested.connect(lambda: self.handle_navigation("settings"))
    
    def initialize_app(self):
        """Initialize the application based on authentication status"""
        if self.user_model.is_authenticated:
            self.view.show_app()
            self.view.show_dashboard()
        else:
            self.view.show_auth()
    
    def handle_login(self, email, username):
        """
        Handle successful login
        
        Args:
            email: User's email
            username: User's username
        """
        # Show main application screen
        self.view.show_app()
        
        # Navigate to dashboard
        self.view.show_dashboard()
    
    def handle_register(self, email, username, password):
        """
        Handle successful registration
        
        Args:
            email: User's email
            username: User's username
            password: User's password
        """
        # Show main application screen
        self.view.show_app()
        
        # Navigate to dashboard
        self.view.show_dashboard()
    
    def handle_logout(self):
        """Handle logout action"""
        # Show authentication screen
        self.view.show_auth()
    
    def handle_navigation(self, target):
        """
        Handle navigation between different screens
        
        Args:
            target: String identifier for the target screen
        """
        if target == "dashboard":
            self.view.show_dashboard()
        
        elif target == "portfolio":
            self.view.show_portfolio()
        
        elif target == "stocks":
            self.view.show_stocks()
        
        elif target == "transactions":
            self.view.show_transactions()
        
        elif target == "settings":
            self.view.show_settings()
    
    def model_updated(self):
        """
        Called when the user model is updated
        This method is required for the observer pattern
        """
        # If user is authenticated, show main app
        # Otherwise, show auth screen
        if self.user_model.is_authenticated:
            self.view.show_app()
        else:
            self.view.show_auth()