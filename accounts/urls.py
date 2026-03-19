from django.urls import path
from .views import RegisterView, LoginView, StatusView, VerifyTokenView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('status/', StatusView.as_view()),
    path('verify-token/', VerifyTokenView.as_view()),
]
