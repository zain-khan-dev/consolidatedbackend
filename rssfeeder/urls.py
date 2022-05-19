from django.urls import path
from . import views


urlpatterns = [
    path("rssFromChannels/", views.RssChannels.as_view()),
    path("rssFromURL/", views.RssFromURL.as_view()),
    path('users/', views.SignupView.as_view()),
]


