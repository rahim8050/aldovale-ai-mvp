from django.urls import path
from . import views

urlpatterns = [
    path("auth/token/", views.token_exchange, name="token-exchange"),
    path("chat/session/", views.session_create, name="session-create"),
    path("chat/message/", views.chat_message, name="chat-message"),
    path("admin/ingest/", views.ingest_data, name="admin-ingest"),
]
