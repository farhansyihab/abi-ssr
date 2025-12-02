from django.shortcuts import render
from .models import HomePage


def home_page_context(request):
    context = {}
    # Add countdown to context if needed
    return context