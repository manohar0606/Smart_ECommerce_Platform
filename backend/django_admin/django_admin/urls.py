"""
URL configuration for django_admin project.
"""

from django.contrib import admin
from django.urls import path

from orders.views import analytics_dashboard


urlpatterns = [
    path("admin/analytics/", analytics_dashboard, name="analytics"),
    path("admin/", admin.site.urls),
]