from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Notification(models.Model):
    class Level(models.TextChoices):
        INFO = "info"
        SUCCESS = "success"
        WARNING = "warning"
        ERROR = "error"

    class Type(models.TextChoices):
        BOOKING_CREATED   = "booking_created"
        STATUS_CHANGED    = "status_changed" 
        BOOKING_UPDATED   = "booking_updated"
        BOOKING_DELETED   = "booking_deleted"
        PENDING_APPROVALS = "pending_approvals"
        CONFLICT_FLAG     = "conflict_flag"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=50, choices=Type.choices)
    level = models.CharField(max_length=10, choices=Level.choices, default=Level.INFO)

    target_ct = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_ct", "target_id")

    message = models.TextField(blank=True)
    payload = models.JSONField(default=dict, blank=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    dedupe_key = models.CharField(max_length=120, blank=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]