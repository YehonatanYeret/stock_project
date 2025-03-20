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
        #call the function to generate AI response
        msg = self.model.generate_ai_response(message_content)
        # Add to view
        self.view.add_response(msg.content)