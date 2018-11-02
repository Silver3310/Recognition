"""Recognition URL Configuration

The `urlpatterns` list routes URLs to views of the letter recognition app.
"""
from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', views.RequestViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]
