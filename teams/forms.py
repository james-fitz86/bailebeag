from django import forms
from .models import Team
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['age_group', 'gender', 'sport', 'coach']
        widgets = {
            'age_group': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'sport': forms.Select(attrs={'class': 'form-control'}),
            'coach': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['coach'].queryset = CustomUser.objects.filter(role='coach')
