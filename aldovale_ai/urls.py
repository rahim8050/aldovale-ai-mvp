# aldovale_ai/urls.py

from django.urls import path
from .views import TokenObtainView, ChatSessionView

app_name = "aldovale_ai"

urlpatterns = [
    path("auth/token/", TokenObtainView.as_view(), name="token_obtain"),
    path("chat/session/", ChatSessionView.as_view(), name="chat_session"),
]
