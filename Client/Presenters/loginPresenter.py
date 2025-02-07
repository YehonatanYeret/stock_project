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
        
        # Authenticate via API call (model will handle the HTTP request)
        success, user_id, message = self.model.authenticate(username, password)
        print(message)
        if success:
            # self.view.show_signin_message(message)  # Message from server
            self.controller.switch_to_dashboard()
        else:
            self.view.show_signin_message(message)  # Display error from server

    def signup(self):
        """
        Process signup: get signup data from the view, validate via the model and 
        if successful, animate to login mode and switch to dashboard.
        """
        username = self.view.get_signup_username()
        password = self.view.get_signup_password()
        
        # Call the signup method from the model, which sends the data to the API
        success, user_id, message = self.model.signup(username, password)
        print(message)
        if success:
            # self.view.show_signup_message(message)  # Show success message from server
            self.controller.switch_to_dashboard()
        else:
            self.view.show_signup_message(message)  # Show error message from server
