import pytest
import tkinter as tk
from unittest.mock import patch, MagicMock
from app.views.login import LoginView
from app.models.user import User

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def login_view(root):
    mock_on_success = MagicMock()
    view = LoginView(root, on_login_success=mock_on_success)
    view.pack()
    return view

@patch('app.views.login.auth_service.login')
def test_handle_login_success(mock_login, login_view):
    # Setup mock
    mock_user = User(id=1, username="admin", role="Admin")
    mock_login.return_value = mock_user

    # Simulate user input
    login_view.entry_username.insert(0, "admin")
    login_view.entry_password.insert(0, "admin123")

    # Trigger action
    login_view.handle_login()

    # Assertions
    mock_login.assert_called_once_with("admin", "admin123")
    login_view.on_login_success.assert_called_once_with(mock_user)

@patch('app.views.login.messagebox.showerror')
@patch('app.views.login.auth_service.login')
def test_handle_login_failure(mock_login, mock_showerror, login_view):
    # Setup mock
    mock_login.return_value = None

    # Simulate user input
    login_view.entry_username.insert(0, "wrong")
    login_view.entry_password.insert(0, "wrong")

    # Trigger action
    login_view.handle_login()

    # Assertions
    mock_login.assert_called_once_with("wrong", "wrong")
    login_view.on_login_success.assert_not_called()
    mock_showerror.assert_called_once_with("Error", "Invalid username or password")

@patch('app.views.login.messagebox.showerror')
def test_handle_login_empty_fields(mock_showerror, login_view):
    # Trigger action with empty fields
    login_view.handle_login()

    # Assertions
    mock_showerror.assert_called_once_with("Error", "Please enter both username and password")
    login_view.on_login_success.assert_not_called()
