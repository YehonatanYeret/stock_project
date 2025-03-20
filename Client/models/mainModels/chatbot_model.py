from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional

from services.api_service import ApiService


@dataclass
class ChatMessage:
    """Data class for chat messages"""
    content: str
    timestamp: datetime
    is_user: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "is_user": self.is_user
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        """Create from dictionary format"""
        return cls(
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            is_user=data["is_user"]
        )


class ChatbotModel:
    """Model for the chatbot feature"""

    def __init__(self, api_service=None):
        self.api_service = api_service or ApiService()
        self.message_history: List[ChatMessage] = []
        self.user_id: Optional[int] = None

    def set_user_id(self, user_id: int):
        """Set the current user ID"""
        self.user_id = user_id

    def add_message(self, content: str, is_user: bool) -> ChatMessage:
        """Add a new message to the history"""
        message = ChatMessage(
            content=content,
            timestamp=datetime.now(),
            is_user=is_user
        )
        self.message_history.append(message)
        return message


    def generate_ai_response(self, user_message: str):
        """Generate AI response based on user message"""
        # This is where you would integrate with an actual AI service
        # For now, we'll use simple keyword matching
        status, response = self.api_service.get_AI_response(user_message)
        if status:
            return self.add_message(response, is_user=False)
        else:
            return self.add_message("there is an error. please try again later", is_user=False)
        
    def get_message_history(self) -> List[ChatMessage]:
        """Get the full message history"""
        return self.message_history

    def clear_history(self):
        """Clear the message history"""
        self.message_history = []

    def get_portfolio_data(self) -> Dict[str, Any]:
        """Get user portfolio data from API"""
        if not self.user_id:
            return {"error": "User not authenticated"}

        success, holdings = self.api_service.get_holdings(self.user_id)
        if not success:
            return {"error": "Failed to fetch holdings"}

        success, transactions = self.api_service.get_transactions(self.user_id)
        if not success:
            return {"error": "Failed to fetch transactions"}

        cash_balance = self.api_service.get_cash_balance(self.user_id)

        return {
            "holdings": holdings,
            "transactions": transactions,
            "cash_balance": cash_balance
        }
