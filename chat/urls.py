from django.urls import path
from .views import getMessages

urlpatterns = [
    path('history/<int:course>/', getMessages, name='getMessages'),
]
