from Interfaces.ILogin import *
from Models.loginModel import *

class LoginPresenter:
    def __init__(self, controller, Iview:ILogin, Imodel:LoginModel):
        self.view = Iview
        self.model = Imodel
        self.controller = controller

    def login(self):
        username = self.view.get_username()
        password = self.view.get_password()
        #בדיקת האימות לא צריכה להיות פה !!!
        if self.model.authenticate(username, password):
            self.view.show_message("Login successful!")
            self.controller.switch_to_dashboard()
        else:
            self.view.show_message("Invalid username or password. Please try again.")
