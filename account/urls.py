from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    path('login/', LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_complete/', CompleteResetPassword.as_view()),
]
