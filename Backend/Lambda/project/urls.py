from wambda.urls import Path, Router
from .views import home

urlpatterns = [
  Path("", home, name="home"),
  Router("accounts", "accounts.urls", name="accounts"),
  Router("api", "api.urls", name="api"),
]