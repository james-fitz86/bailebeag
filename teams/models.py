from django.db import models
from django.conf import settings

# Create your models here.
class Team(models.Model):
    AGE_GROUP_CHOICES = [
        ('U7', 'Under 7'),
        ('U8', 'Under 8'),
        ('U9', 'Under 9'),
        ('U10', 'Under 10'),
        ('U11', 'Under 11'),
        ('U12', 'Under 12'),
        ('U13', 'Under 13'),
        ('U14', 'Under 14'),
        ('U15', 'Under 15'),
        ('U16', 'Under 16'),
        ('Minor', 'Minor'),
        ('U21', 'Under 21'),
        ('Reserve', 'Reserve'),
        ('Senior', 'Senior'),
    ]

    GENDER_CHOICES = [
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('men', 'Men'),
        ('women', 'Women'),
        ('mixed', 'Mixed')
    ]

    SPORT_CHOICES = [
        ('football', 'Football'),
        ('hurling', 'Hurling'),
        ('camogie', 'Camogie'),
    ]

    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    sport = models.CharField(max_length=10, choices=SPORT_CHOICES)

    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': 'coach'},
        related_name='coached_teams'
    )

    def __str__(self):
        return f"{self.age_group} {self.get_gender_display()} ({self.get_sport_display()})"