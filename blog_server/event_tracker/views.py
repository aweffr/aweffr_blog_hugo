from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import Event, EventHealth
from .serializers import HealthSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


def fake_vue_index(request: HttpRequest):
    return render(request, 'index_vue.html', {'debug': settings.DEBUG})
