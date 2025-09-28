from wambda.urls import Path
from .views import (
    login_view, signup_view, logout_view, verify_view,
    change_password_view, forgot_password_view, reset_password_view,
    user_profile_view, delete_account_view, auth_status
)

urlpatterns = [
    Path("login", login_view, name="login"),
    Path("signup", signup_view, name="signup"),
    Path("logout", logout_view, name="logout"),
    Path("verify", verify_view, name="verify"),
    Path("change-password", change_password_view, name="change_password"),
    Path("forgot-password", forgot_password_view, name="forgot_password"),
    Path("reset-password", reset_password_view, name="reset_password"),
    Path("profile", user_profile_view, name="profile"),
    Path("delete-account", delete_account_view, name="delete_account"),
    Path("status", auth_status, name="status"),
]