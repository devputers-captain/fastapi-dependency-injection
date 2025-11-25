"""
Admin router demonstrating router-level dependencies.
All routes in this router automatically require admin authentication.
"""
from app.dependencies import verify_admin
from app.services import UserService
from fastapi import APIRouter, Depends

# Router-level dependency: Applied to ALL routes in this router
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_admin)]  # 👈 ALL routes require admin auth
)


@router.get("/stats")
def get_system_stats(user_service: UserService = Depends(UserService)):
    """
    Get system statistics (admin only).
    
    No need to add verify_admin dependency here - 
    it's automatically applied via router-level dependency!
    
    Try with header: Authorization: admin-token-123
    """
    users_data = user_service.users
    return {
        "total_users": len(users_data),
        "user_types": {
            "admin": sum(1 for u in users_data.values() if u["account_type"] == "admin"),
            "standard": sum(1 for u in users_data.values() if u["account_type"] == "standard"),
        }
    }


@router.get("/users/list")
def list_all_users(user_service: UserService = Depends(UserService)):
    """
    List all users in the system (admin only).
    
    This route also automatically requires admin authentication
    because of router-level dependency.
    
    Try with header: Authorization: admin-token-123
    """
    return {
        "users": list(user_service.users.values()),
        "count": len(user_service.users)
    }

