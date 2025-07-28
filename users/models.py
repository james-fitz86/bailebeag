from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('coach', 'Coach'),
        ('manager', 'Booking Manager'),
        ('chairman', 'Chairman'),
        ('secretary', 'Secretary'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)