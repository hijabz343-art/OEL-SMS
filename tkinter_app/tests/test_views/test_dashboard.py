import pytest
import tkinter as tk
from unittest.mock import patch, MagicMock
from app.views.dashboard import DashboardView
from app.models.user import User

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@patch('app.views.dashboard.auth_service.get_current_user')
def test_dashboard_admin_role(mock_get_user, root):
    mock_get_user.return_value = User(id=1, username="admin", role="Admin")
    view = DashboardView(root, on_logout=MagicMock())
    
    # In Tkinter, getting all button texts from a container requires iterating
    buttons = [w for w in view.sidebar.winfo_children() if isinstance(w, tk.Button)]
    button_texts = [btn.cget("text") for btn in buttons]
    
    assert "Students" in button_texts
    assert "Teachers" in button_texts
    assert "Classes" in button_texts
    assert "Attendance" in button_texts
    assert "Fees" in button_texts
    assert "Reports" in button_texts

@patch('app.views.dashboard.auth_service.get_current_user')
def test_dashboard_teacher_role(mock_get_user, root):
    mock_get_user.return_value = User(id=2, username="teacher", role="Teacher")
    view = DashboardView(root, on_logout=MagicMock())
    
    buttons = [w for w in view.sidebar.winfo_children() if isinstance(w, tk.Button)]
    button_texts = [btn.cget("text") for btn in buttons]
    
    assert "Students" in button_texts
    assert "Teachers" not in button_texts # Teacher should not see Teachers
    assert "Classes" in button_texts
    assert "Attendance" in button_texts
    assert "Fees" not in button_texts     # Teacher should not see Fees
    assert "Reports" in button_texts
