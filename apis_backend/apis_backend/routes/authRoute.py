
# make all the routes related to authentication

from django.urls import path
from ..controllers.AuthController import AuthController
from ..validators.AuthValidator import AuthValidator


urlpatterns = [
    path('register', AuthController.as_view(), name="register"),
    path('login', AuthController.as_view(), name="login"),
    path('admin/login', AuthController.as_view() , name="adminLogin"),
    path('refresh-token', AuthController.as_view() , name="refreshToken"),
]

