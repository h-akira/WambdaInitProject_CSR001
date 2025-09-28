from wambda.urls import Path
from .views import hello_api

urlpatterns = [
  Path("hello", hello_api, name="hello"),
]