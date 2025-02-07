from Models.portfolioModel import *

class PortfolioPresenter:
    def __init__(self, controller, model, view):
        self.view = view
        self.model = model
        self.controller = controller

        # Update the view with the user_id
        self.view.update_user_id(self.model.user_id)

