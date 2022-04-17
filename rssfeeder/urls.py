from django.urls import path
from . import views


urlpatterns = [
    path("index/", views.index.as_view()),
    path('users/', views.SignupView.as_view())
]
