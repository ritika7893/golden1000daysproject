from django.urls import path
from .views import Intervention4CreateAPIView,Intervention3CreateAPIView,Intervention2CreateAPIView,QuestionnaireInterventionAPIView,CandidateDetailAPIView,LoginAPIView, RefreshTokenAPIView,ResetPasswordAPIView,UserListAPIView,CandidateAPIView,Intervention1CreateAPIView
urlpatterns = [
    path('login/',LoginAPIView.as_view(),name='login'),
    path('refresh-token/', RefreshTokenAPIView.as_view(), name='refresh_token'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('users-list/', UserListAPIView.as_view(), name='users-list'),
    path("candidate-reg/",CandidateAPIView.as_view(),name="candidate-api"),
    path("candidate/details/",CandidateDetailAPIView.as_view(),name="candidate-details"),
    path('intervention1/create/', Intervention1CreateAPIView.as_view(), name='intervention1-create'),
    path("questionnaire-intervention/",QuestionnaireInterventionAPIView.as_view(),name="questionnaire-intervention"),
    path( 'intervention2/create/',Intervention2CreateAPIView.as_view(),name='intervention2-create'),
    path("intervention3/create/",Intervention3CreateAPIView.as_view(),name="intervention3-create"),
    path("intervention4/create/",Intervention4CreateAPIView.as_view(),name="intervention4-create"),
]