from app.dependencies import Settings, get_current_user, get_settings, verify_admin
from app.services import UserService
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile")
def user_profile(
    user: dict = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
    user_service: UserService = Depends(UserService),
):
    """
    Get the current user's profile.
    
    Demonstrates multiple dependency injection:
    - get_current_user: Function-based dependency (authentication)
    - get_settings: Function returning class instance (configuration)
    - UserService: Direct class injection (business logic)
    """
    data = user_service.fetch_user_data(user["username"])
    return {
        "app": settings.app_name,
        "version": settings.version,
        "profile": data,
    }


@router.get("/dashboard")
def user_dashboard(
    admin: dict = Depends(verify_admin),
    user_service: UserService = Depends(UserService),
):
    """
    Admin dashboard endpoint demonstrating nested dependencies.
    
    Dependency chain: verify_admin → verify_token → Header extraction
    
    Only accessible with admin token.
    Try with header: Authorization: admin-token-123
    """
    return {
        "message": f"Welcome to admin dashboard, {admin['username']}!",
        "role": admin["role"],
        "total_users": len(user_service.users),
        "all_users": list(user_service.users.keys())
    }
