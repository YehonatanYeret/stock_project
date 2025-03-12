import json
import os
from pathlib import Path

class SessionService:
    def __init__(self):
        self._session_file = self._get_session_file_path()
    
    def _get_session_file_path(self):
        """Get the path to the session file"""
        app_data_dir = Path.home() / ".stockapp"
        if not app_data_dir.exists():
            app_data_dir.mkdir(exist_ok=True)
        return app_data_dir / "session.json"
    
    def save_session(self, user_id, token):
        """Save the user session to a file"""
        session_data = {
            "user_id": user_id,
            "token": token
        }
        try:
            with open(self._session_file, 'w') as f:
                json.dump(session_data, f)
            return True
        except Exception as e:
            print(f"Error saving session: {str(e)}")
            return False
    
    def load_session(self):
        """Load the user session from a file"""
        if not os.path.exists(self._session_file):
            return None
        
        try:
            with open(self._session_file, 'r') as f:
                session_data = json.load(f)
            return session_data
        except Exception as e:
            print(f"Error loading session: {str(e)}")
            return None
    
    def clear_session(self):
        """Clear the user session (logout)"""
        if os.path.exists(self._session_file):
            try:
                os.remove(self._session_file)
                return True
            except Exception as e:
                print(f"Error clearing session: {str(e)}")
                return False
        return True