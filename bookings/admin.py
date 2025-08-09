from django.contrib import admin
from .models import Pitch, Booking

# Register your models here.
@admin.register(Pitch)
class PitchAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_public')
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'pitch', 'name', 'start_time', 'end_time', 'status', 'method', 'submitted_at'
    )
    list_filter = ('pitch', 'status', 'method', 'start_time')
    search_fields = ('name', 'email', 'phone')
    date_hierarchy = 'start_time'
    ordering = ('-submitted_at',)