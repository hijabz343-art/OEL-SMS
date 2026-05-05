import pytest
from unittest.mock import patch
from app.services.auth import AuthService

@pytest.fixture
def auth_service():
    return AuthService()

@patch('app.services.auth.db.fetch_one')
def test_login_success_admin(mock_fetch_one, auth_service):
    # Mocking a successful database return
    mock_fetch_one.return_value = {
        'id': 1,
        'username': 'admin',
        'password': 'admin123',
        'role': 'Admin'
    }
    
    user = auth_service.login('admin', 'admin123')
    
    assert user is not None
    assert user.username == 'admin'
    assert user.role == 'Admin'
    assert auth_service.get_current_user() == user
    mock_fetch_one.assert_called_once_with(
        "SELECT id, username, password, role FROM users WHERE username = %s AND password = %s",
        ('admin', 'admin123')
    )

@patch('app.services.auth.db.fetch_one')
def test_login_success_teacher(mock_fetch_one, auth_service):
    # Mocking a successful database return for Teacher
    mock_fetch_one.return_value = {
        'id': 2,
        'username': 'teacher1',
        'password': 'password',
        'role': 'Teacher'
    }
    
    user = auth_service.login('teacher1', 'password')
    
    assert user is not None
    assert user.username == 'teacher1'
    assert user.role == 'Teacher'

@patch('app.services.auth.db.fetch_one')
def test_login_failure(mock_fetch_one, auth_service):
    # Mocking a failed database return
    mock_fetch_one.return_value = None
    
    user = auth_service.login('wrong', 'wrong')
    
    assert user is None
    assert auth_service.get_current_user() is None

def test_logout(auth_service):
    auth_service.current_user = "Dummy User"
    auth_service.logout()
    assert auth_service.get_current_user() is None
