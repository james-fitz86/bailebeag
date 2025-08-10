from django.db import transaction
from .models import Notification
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime

def fmt(dt):
    return timezone.localtime(dt).strftime("%H:%M %d/%m/%y")

def create_notification(*, recipient, type, level=Notification.Level.INFO, target=None, message="", payload=None, dedupe_key=""):
    payload = payload or {}
    def _make():
        Notification.objects.create(
            recipient=recipient,
            type=type,
            level=level,
            target=target,
            message=message,
            payload=payload,
            dedupe_key=dedupe_key,
        )
    transaction.on_commit(_make)

def for_booking_created(booking):
    if not booking.created_by_id:
        return
    create_notification(
        recipient=booking.created_by,
        type=Notification.Type.BOOKING_CREATED,
        level=Notification.Level.SUCCESS,
        target=booking,
        message=(
            f"Booking for {booking.pitch.name} from {fmt(booking.start_time)} "
            f"to {fmt(booking.end_time)} was created, booking status is currently "
            f"‘{booking.status}’."
        ),
        payload={"status": booking.status},
    )

def for_status_changed(booking, old, new):
    create_notification(
        recipient=booking.created_by,
        type=Notification.Type.STATUS_CHANGED,
        level=Notification.Level.SUCCESS if new == "approved" else Notification.Level.WARNING if new == "conflicting" else Notification.Level.ERROR if new == "rejected" else Notification.Level.INFO,
        target=booking,
        message=(
            f"Booking for {booking.pitch.name} from {fmt(booking.start_time)} "
            f"to {fmt(booking.end_time)} has differnet status: {old} → {new}."
        ),
        payload={"old_status": old, "new_status": new},
    )

def for_booking_updated(booking, changed_fields):
    create_notification(
        recipient=booking.created_by,
        type=Notification.Type.BOOKING_UPDATED,
        level=Notification.Level.INFO,
        target=booking,
        message=f"Booking for {booking.pitch.name} from {fmt(booking.start_time)} to {fmt(booking.end_time)} was updated.",
        payload={"changed_fields": changed_fields},
    )

def for_booking_deleted(booking_snapshot):
    User = get_user_model()
    user_id = booking_snapshot.get("user_id")
    if not user_id:
        return

    try:
        recipient = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return
    
    start_str = fmt(booking_snapshot.get("start_time"))
    end_str = fmt(booking_snapshot.get("end_time"))
    pitch_name = booking_snapshot.get("pitch_name", "this pitch")
    
    payload = booking_snapshot.copy()
    for key in ("start_time", "end_time"):
        val = payload.get(key)
        if isinstance(val, datetime):
            payload[key] = val.isoformat()
    
    create_notification(
        recipient=recipient,
        type=Notification.Type.BOOKING_DELETED,
        level=Notification.Level.ERROR,
        target=None,
        message=f"Booking for {pitch_name} from {start_str} to {end_str} was deleted.",
        payload=payload,
    )
