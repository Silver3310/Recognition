"""prv_server URL Configuration

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(
        '32hj4f31f04/',
        admin.site.urls
    ),
    # API endpoint
    path(
        'api/',
        include('recognition.api.urls')
    )
]
