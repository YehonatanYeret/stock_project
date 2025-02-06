from abc import ABC, abstractmethod

# Dummy ILogin interface (if you have one, replace accordingly)
class ILogin(ABC):
    @abstractmethod
    def get_username(self): pass

    @abstractmethod
    def get_password(self): pass
    
    @abstractmethod
    def show_signin_message(self, message): pass
    
    @abstractmethod
    def get_signup_username(self): pass
    
    @abstractmethod
    def get_signup_password(self): pass
    
    @abstractmethod
    def show_signup_message(self, message): pass