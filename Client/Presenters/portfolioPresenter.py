#from Interfaces.ILogin import *
from Models.portfolioModel import *

class PortfolioPresenter:
    def __init__(self, controller, PortfolioModel, PortfolioView):
        self.view = PortfolioView
        self.model = PortfolioModel
        self.controller = controller

