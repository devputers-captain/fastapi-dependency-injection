class UserService:
    """Service for handling user operations"""
    
    def __init__(self):
        # Simulated database
        self.users: dict[str, dict[str, str]] = {
            "admin": {
                "username": "admin",
                "account_type": "admin",
                "status": "active",
            },
            "standard": {
                "username": "standard",
                "account_type": "standard",
                "status": "active",
            }
        }
    
    def fetch_user_data(self, username: str) -> dict[str, str] | None:
        """Fetch user data from the database"""
        return self.users.get(username)

