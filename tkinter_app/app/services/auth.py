from app.services.db_service import db
from app.models.user import User

class AuthService:
    def __init__(self):
        self.current_user = None

    def login(self, username, password):
        """
        Attempts to log in a user with the given credentials.
        Returns a User object if successful, else None.
        """
        query = "SELECT id, username, password, role FROM users WHERE username = %s AND password = %s"
        result = db.fetch_one(query, (username, password))
        
        if result:
            self.current_user = User(
                id=result['id'],
                username=result['username'],
                role=result['role']
            )
            return self.current_user
        
        return None

    def logout(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user

# Global auth service instance
auth_service = AuthService()
