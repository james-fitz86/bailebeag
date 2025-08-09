from django.contrib import admin
from .models import Team
# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('age_group', 'gender', 'sport', 'coach')
    list_filter = ('gender', 'sport', 'age_group')
    search_fields = ('coach__first_name', 'coach__last_name')