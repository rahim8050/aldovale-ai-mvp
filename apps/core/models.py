from django.db import models
from django.utils import timezone
import uuid

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    api_key_hash = models.CharField(max_length=128)
    webhook_url = models.URLField(blank=True, null=True)
    config = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    jwt_jti = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_reply = models.TextField(blank=True, null=True)
    sources = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    embeddings_status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='open')
    external_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
