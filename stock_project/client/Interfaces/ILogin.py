from abc import ABC, abstractmethod

class ILogin(ABC):    
    @abstractmethod
    def get_username(self):
        pass

    @abstractmethod
    def get_password(self):
        pass

    # @abstractmethod
    # def authenticate(self, username, password):
    #     pass