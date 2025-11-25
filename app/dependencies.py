import random

from fastapi import Depends, Header, HTTPException, status

# ===== Function-based Dependencies =====

def get_current_user() -> dict[str, str]:
    """
    Dependency to get the current authenticated user.
    In a real app, this would extract the user from JWT token or session.
    """
    # Simulated authentication - randomly pick a user
    user_types = ["admin", "standard"]
    random_user = random.choice(user_types)
    
    return {
        "username": random_user,
        "account_type": random_user,
        "status": "active",
    }


# ===== Class-based Dependencies =====

class Settings:
    """Application settings"""
    
    def __init__(self):
        self.app_name = "DI Demo App"
        self.version = "1.0.0"


def get_settings() -> Settings:
    """
    Dependency to get application settings.
    In a real app, this would load from environment variables or config files.
    """
    return Settings()


# ===== Nested Dependencies (Chain) =====

def verify_token(authorization: str = Header(None)) -> dict[str, str]:
    """
    First level: Verify authentication token from header.
    In a real app, this would validate JWT tokens.
    """
    # Simulated token validation
    valid_tokens = {
        "admin-token-123": {"username": "admin", "role": "admin"},
        "user-token-456": {"username": "john_doe", "role": "user"},
    }
    
    if not authorization or authorization not in valid_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return valid_tokens[authorization]


def verify_admin(current_user: dict = Depends(verify_token)) -> dict[str, str]:
    """
    Second level: Verify user is admin (depends on verify_token).
    This creates a dependency chain: verify_admin → verify_token
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
