from django.urls import path
from .views import MessageCreateView

urlpatterns = [
    path("messages/", MessageCreateView.as_view(), name="messages"),
]
