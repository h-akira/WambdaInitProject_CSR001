from wambda.urls import Path
from .views import auth_status, hello_api

urlpatterns = [
  Path("auth/status", auth_status, name="auth_status"),
  Path("hello", hello_api, name="hello"),
]