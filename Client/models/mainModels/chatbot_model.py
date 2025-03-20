
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
from services.api_service import ApiService

class ChatbotModel:
    def __init__(self, api_service=None):
        self.api_service = api_service or ApiService()
        self.user_id: Optional[int] = None

    def set_user_id(self, user_id: int):
        self.user_id = user_id

    def generate_ai_response(self, user_message: str):
        # Simulate server delay if needed, e.g., sleep(1)
        status, response = self.api_service.get_AI_response(user_message)
        if status:
            return response
        else:
            return "There is an error. Please try again later."

