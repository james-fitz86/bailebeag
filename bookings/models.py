from django.db import models
from django.conf import settings

# Create your models here.
class Pitch(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Booking(models.Model):
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)

    # For public users or when managers log bookings manually
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # When logged-in users (e.g., coaches or admins) make bookings
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    method = models.CharField(max_length=20, choices=[
        ('web', 'Website'),
        ('phone', 'Phone'),
        ('email', 'Email'),
    ], default='web')

    status = models.CharField(max_length=11, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('conflicting', 'Conflicting'),
    ], default='pending')

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pitch.name} booking on {self.start_time.strftime('%Y-%m-%d %H:%M')}"
