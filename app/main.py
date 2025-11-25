from app.routers import admin, users
from fastapi import Depends, FastAPI, Request

# ===== Global Dependency Example =====

def log_request(request: Request):
    """
    Global dependency: Applied to all routes in the application.
    Useful for logging, rate limiting, or monitoring.
    """
    print(f"📝 Request: {request.method} {request.url.path}")
    # In production, use proper logging:
    # logger.info(f"{request.method} {request.url.path} - {request.client.host}")
    return True


# Create app with global dependency
app = FastAPI(
    title="FastAPI Dependency Injection Example",
    description="Demonstrating all DI patterns: function-based, class-based, nested, router-level, and global",
    version="1.0.0",
    dependencies=[Depends(log_request)]  # 👈 Applied to ALL routes globally
)

# Include routers
app.include_router(users.router)
app.include_router(admin.router)


@app.get("/", tags=["Root"])
def home():
    """
    Root endpoint.
    
    Note: log_request dependency runs automatically for this route too!
    """
    return {
        "message": "FastAPI Dependency Injection Demo",
        "features": {
            "function_based": "get_current_user, get_settings",
            "class_based": "Settings, UserService",
            "nested": "verify_admin → verify_token",
            "router_level": "/admin routes require admin auth",
            "global": "log_request runs on all routes"
        },
        "endpoints": {
            "basic": "/users/profile",
            "nested_dependency": "/users/dashboard (Header: Authorization: admin-token-123)",
            "router_level": "/admin/stats (Header: Authorization: admin-token-123)",
            "docs": "/docs"
        }
    }

