"""consolidatedbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('cnn', views.cnnRSSEngine),
    path('hn', views.getHackerNewsEngine),
    path('nyt', views.getNYTEngine),
    path('tm', views.getTechMemeEngine),
    path('rt', views.getReutersEngine),
    path('tc', views.getTechCrunchEngine),
    path('mit', views.getMITEngine),
    path('wd', views.getWiredEngine),
    path('ieee', views.getIeeeEngine),
    path('ars', views.getARSTechnicaEngine),     # remove ars wont support it
    path("bbc", views.getBBCEngine),
    path("htg", views.getHowToGeekEngine)
]
