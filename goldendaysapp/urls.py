from django.urls import path
from .views import LoginAPIView, RefreshTokenAPIView,ResetPasswordAPIView,UserListAPIView,CandidateAPIView
urlpatterns = [
    path('login/',LoginAPIView.as_view(),name='login'),
    path('refresh-token/', RefreshTokenAPIView.as_view(), name='refresh_token'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('users-list/', UserListAPIView.as_view(), name='users-list'),
    path("candidate-reg/",CandidateAPIView.as_view(),name="candidate-api"),

]