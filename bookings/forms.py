from django import forms
from .models import Booking, Pitch

from django import forms
from .models import Booking, Pitch

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pitch', 'name', 'email', 'phone', 'start_time', 'end_time', 'method']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Restricts pitch options based on user
        if self.user and self.user.is_authenticated:
            role = getattr(self.user, 'role', None)
            
            if role in ['coach', 'chairman', 'secretary', 'manager']:
                self.fields['pitch'].queryset = Pitch.objects.all()
            else:
                self.fields['pitch'].queryset = Pitch.objects.filter(name__icontains='Astro')

            # Restricts method choice only to manager, all other users are default web in views, so don't need this choice
            if role == 'manager':
                self.fields['method'].choices = [
                    ('phone', 'Phone'),
                    ('email', 'Email'),
                ]
            else:
                self.fields['method'].widget = forms.HiddenInput()
                self.fields['method'].initial = 'web'

            for field in ['name', 'email', 'phone']:
                self.fields[field].required = False
                self.fields[field].widget = forms.HiddenInput()
        else:
            self.fields['method'].widget = forms.HiddenInput()
            self.fields['method'].initial = 'web'
            self.fields['pitch'].queryset = Pitch.objects.filter(name__icontains='Astro')