# Presenters/loginPresenter.py

from Models.loginModel import LoginModel

class LoginPresenter:
    def __init__(self, controller, view, model: LoginModel):
        self.controller = controller
        self.view = view
        self.model = model

    def login(self):
        """
        Process login: get credentials from the view and authenticate via the model.
        """
        username = self.view.get_username()
        password = self.view.get_password()
        if self.model.authenticate(username, password):
            self.view.show_signin_message("Login successful!")
            self.controller.switch_to_dashboard()
        else:
            self.view.show_signin_message("Invalid username or password. Please try again.")

    def signup(self):
        """
        Process signup: get signup data from the view, validate via the model and 
        if successful, animate to login mode and switch to dashboard.
        """
        username = self.view.get_signup_username()
        password = self.view.get_signup_password()
        success, message = self.model.signup(username, password)
        if success:
            print(message)
            self.view.clear_signup_fields()
            # Animate to login mode if currently in signup mode.
            self.controller.switch_to_dashboard()
        else:
            # If signup fails, display the error and remain in signup mode.
            self.view.show_signup_message(message)
