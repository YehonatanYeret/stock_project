from Interfaces.ILogin import *
from Models.loginModel import *

class LoginPresenter:
    def __init__(self, Iview:ILogin, Imodel:LoginModel):
        self.view = Iview
        self.model = Imodel

    def login(self):
        username = self.view.get_username()
        password = self.view.get_password()
        #בדיקת האימות לא צריכה להיות פה !!!
        if self.model.authenticate(username, password):
            self.view.show_signin_message("Login successful!")
        else:
            self.view.show_signin_message("Invalid username or password. Please try again.")


    def signup(self):
        self.view.show_signup_message("Sign up successful!")
        print("Sign up successful!")
