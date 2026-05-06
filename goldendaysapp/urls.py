from django.urls import path
from .views import LoginAPIView, RefreshTokenAPIView, StudentRegAPIView
urlpatterns = [
    path('login/',LoginAPIView.as_view(),name='login'),
    path('refresh-token/', RefreshTokenAPIView.as_view(), name='refresh_token'),
]