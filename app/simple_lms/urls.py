"""
URL configuration for simple_lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from lms.api import router as lms_router

# Inisialisasi API
api = NinjaAPI(title="Simple LMS API")

# Register router LMS
api.add_router("/lms/", lms_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
