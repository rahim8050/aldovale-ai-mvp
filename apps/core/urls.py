from django.urls import path
from .views import (
    TokenExchangeView,
    SessionCreateView,
    ChatMessageView,
    AdminIngestView,
)

urlpatterns = [
    path("auth/token/", TokenExchangeView.as_view(), name="token-exchange"),
    path("chat/session/", SessionCreateView.as_view(), name="session-create"),
    path("chat/message/", ChatMessageView.as_view(), name="chat-message"),
    path("admin/ingest/", AdminIngestView.as_view(), name="admin-ingest"),
]
