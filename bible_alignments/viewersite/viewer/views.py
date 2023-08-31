"""Views for the viewer app."""

# from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """Render a hello world."""
    return HttpResponse("Hello viewing world.")
