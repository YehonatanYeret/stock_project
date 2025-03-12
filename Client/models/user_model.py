class UserModel:
    def __init__(self):
        self._id = None
        self._email = None
        self._username = None
        self._token = None
        self._is_authenticated = False
        self._portfolio_id = None
        self._observers = []
    
    def register_observer(self, observer):
        """Add an observer to be notified of model changes"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer):
        """Remove an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self):
        """Notify all observers of a change in the model"""
        for observer in self._observers:
            observer.model_updated()
    
    def set_user_data(self, user_data):
        """Set user data from API response"""
        self._id = user_data.get('id')
        self._email = user_data.get('email')
        self._username = user_data.get('username')
        self._portfolio_id = user_data.get('portfolioId')
        self._is_authenticated = True
        self.notify_observers()
    
    def set_token(self, token):
        """Set authentication token"""
        self._token = token
        
    def clear_user_data(self):
        """Clear user data (logout)"""
        self._id = None
        self._email = None
        self._username = None
        self._token = None
        self._is_authenticated = False
        self._portfolio_id = None
        self.notify_observers()
    
    @property
    def id(self):
        return self._id
    
    @property
    def email(self):
        return self._email
    
    @property
    def username(self):
        return self._username
    
    @property
    def token(self):
        return self._token
    
    @property
    def is_authenticated(self):
        return self._is_authenticated
    
    @property
    def portfolio_id(self):
        return self._portfolio_id