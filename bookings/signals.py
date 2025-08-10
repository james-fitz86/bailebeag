from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import Booking
from alerts.services import (
    for_booking_created, for_status_changed, for_booking_updated, for_booking_deleted
)

CORE_FIELDS = ["pitch_id", "start_time", "end_time"]

def _diff_core(old, new):
    changed = []
    for f in CORE_FIELDS:
        if getattr(old, f) != getattr(new, f):
            changed.append("pitch" if f == "pitch_id" else f)
    return changed

@receiver(pre_save, sender=Booking)
def booking_pre_save(sender, instance: Booking, **kwargs):
    if instance.pk:
        try:
            instance._old = sender.objects.only(
                "status", "pitch_id", "start_time", "end_time"
            ).get(pk=instance.pk)
        except sender.DoesNotExist:
            instance._old = None
    else:
        instance._old = None

@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance: Booking, created, **kwargs):
    if created:
        for_booking_created(instance)
        return

    old = getattr(instance, "_old", None)
    if not old:
        return

    if old.status != instance.status:
        for_status_changed(instance, old.status, instance.status)

    changed_core = _diff_core(old, instance)
    if changed_core:
        for_booking_updated(instance, changed_core)

    if hasattr(instance, "_old"):
        delattr(instance, "_old")

@receiver(pre_delete, sender=Booking)
def booking_pre_delete(sender, instance: Booking, **kwargs):
    snap = {
        "id": instance.id,
        "user_id": instance.created_by_id,
        "pitch_name": instance.pitch.name,
        "start_time": instance.start_time,
        "end_time": instance.end_time,
        "status": instance.status,
    }
    for_booking_deleted(snap)

