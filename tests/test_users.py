from app.dependencies import get_current_user, verify_admin, verify_token
from app.main import app
from app.services import UserService
from fastapi.testclient import TestClient

client = TestClient(app)


# ===== Mock Functions =====

def fake_user() -> dict[str, str]:
    """Mock user for testing"""
    return {
        "username": "test-user",
        "account_type": "standard",
        "status": "active"
    }


def fake_admin() -> dict[str, str]:
    """Mock admin user for testing"""
    return {
        "username": "test-admin",
        "role": "admin"
    }


class MockUserService(UserService):
    """Mock service for testing"""
    
    def __init__(self):
        super().__init__()
        # Add test user to the mock database
        self.users["test-user"] = {
            "username": "test-user",
            "account_type": "standard",
            "status": "active"
        }


# ===== Tests =====

def test_profile():
    """Test basic endpoint with function and class dependencies"""
    # Override dependencies with mocks
    app.dependency_overrides[get_current_user] = fake_user
    app.dependency_overrides[UserService] = MockUserService
    
    response = client.get("/users/profile")
    data = response.json()
    
    assert response.status_code == 200
    assert data["profile"]["username"] == "test-user"
    assert data["profile"]["account_type"] == "standard"
    assert data["app"] == "DI Demo App"
    
    # Clean up
    app.dependency_overrides = {}


def test_admin_dashboard_with_nested_dependency():
    """Test nested dependencies (verify_admin → verify_token)"""
    # Override the nested dependency chain
    app.dependency_overrides[verify_admin] = fake_admin
    app.dependency_overrides[UserService] = MockUserService
    
    response = client.get("/users/dashboard")
    data = response.json()
    
    assert response.status_code == 200
    assert data["role"] == "admin"
    assert "total_users" in data
    
    # Clean up
    app.dependency_overrides = {}


def test_admin_dashboard_unauthorized():
    """Test nested dependency without admin access"""
    response = client.get("/users/dashboard")
    
    # Should fail without proper authentication
    assert response.status_code == 401


def test_router_level_dependency():
    """Test router-level dependency (admin routes)"""
    # Override verify_admin to allow access
    app.dependency_overrides[verify_admin] = fake_admin
    
    response = client.get("/admin/stats")
    data = response.json()
    
    assert response.status_code == 200
    assert "total_users" in data
    assert "user_types" in data
    
    # Clean up
    app.dependency_overrides = {}


def test_router_level_dependency_unauthorized():
    """Test router-level dependency blocks unauthorized access"""
    response = client.get("/admin/stats")
    
    # Should fail without admin authentication
    assert response.status_code == 401


def test_global_dependency():
    """Test that global dependency (log_request) doesn't break routes"""
    response = client.get("/")
    
    # Global dependency should run but not affect response
    assert response.status_code == 200
    assert "message" in response.json()
