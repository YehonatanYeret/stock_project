from PySide6.QtCore import QObject, Slot
class ChatbotPresenter(QObject):
    """Presenter for the Chatbot feature."""

    def __init__(self, model, view, user_id=None):
        super().__init__()
        self.view = view
        self.model = model
        if user_id:
            self.model.set_user_id(user_id)
        self.view.send_message_signal.connect(self.handle_user_message)

    def initialize(self):
        """Initialize the chatbot with a welcome message."""
        welcome_message = "Hello! I'm your AI trading assistant. How can I help you today?"
        self.view.add_response(welcome_message)

    @Slot(str)
    def handle_user_message(self, message_content: str):
        """Handle incoming user messages."""
        response = self.model.generate_ai_response(message_content)
        self.view.add_response(response)
