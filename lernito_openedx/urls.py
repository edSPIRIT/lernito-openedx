"""
URLs for lernito_openedx.
"""
from django.urls import re_path  # pylint: disable=unused-import
from django.views.generic import TemplateView  # pylint: disable=unused-import
from django.urls import path
from .views import LernitoWebhookView

urlpatterns = [
    path('webhook/', LernitoWebhookView.as_view(), name='lernito-webhook'),
]
