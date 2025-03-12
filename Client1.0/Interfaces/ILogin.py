from abc import ABC, abstractmethod

class ILogin(ABC):
    """ 
    Interface defining the structure for authentication methods.
    This should be implemented by any class handling user login/signup.
    """
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