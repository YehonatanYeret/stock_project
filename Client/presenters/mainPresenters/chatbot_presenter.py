from typing import Dict, Any

from PySide6.QtCore import QObject, Signal, Slot, QTimer


class ChatbotPresenter(QObject):
    """Presenter for the Chatbot feature"""

    def __init__(self, model, view, user_id=None):
        super().__init__()
        self.view = view
        self.model = model

        # Set the user ID
        if user_id:
            self.model.set_user_id(user_id)

        # Connect signals
        self.view.send_message_signal.connect(self.handle_user_message)

    def initialize(self):
        """Initialize the chatbot with a welcome message"""
        welcome_message = "Hello! I'm your AI trading assistant. How can I help you today?"
        message = self.model.add_message(welcome_message, is_user=False)
        self.view.add_response(message.content)

    @Slot(str)
    def handle_user_message(self, message_content: str):
        """Handle incoming user messages"""
        # Add to model
        self.model.add_message(message_content, is_user=True)

        # Simulate processing delay
        QTimer.singleShot(500, lambda: self._generate_ai_response(message_content))

    def _generate_ai_response(self, user_message: str):
        """Generate AI response based on user message"""
        # This is where you would integrate with an actual AI service
        # For now, we'll use simple keyword matching

        message_lower = user_message.lower()

        # Get portfolio data when relevant
        portfolio_data = None
        if any(word in message_lower for word in ["portfolio", "holdings", "balance"]):
            portfolio_data = self.model.get_portfolio_data()

        # Simple response logic
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            response = "Hello! How can I assist with your trading today?"

        elif any(word in message_lower for word in ["portfolio", "holdings"]):
            if portfolio_data and "error" not in portfolio_data:
                holdings = portfolio_data["holdings"]
                cash = portfolio_data["cash_balance"]
                response = f"You currently have ${cash:.2f} in cash and {len(holdings)} different stocks in your portfolio."
            else:
                response = "I can analyze your portfolio. Would you like to see your current holdings or get recommendations?"

        elif any(word in message_lower for word in ["market", "trend"]):
            response = "The market has been showing mixed signals lately. Which sector are you interested in?"

        elif any(word in message_lower for word in ["buy", "sell", "trade"]):
            response = "I'm a mock AI assistant. In a real application, I would provide trading recommendations based on your portfolio and market analysis."

        else:
            response = "I'm a mock AI assistant. In a real application, I would provide intelligent responses to your questions about trading and market analysis."

        # Add to model
        message = self.model.add_message(response, is_user=False)

        # Send response back to view
        self.view.add_response(message.content)
