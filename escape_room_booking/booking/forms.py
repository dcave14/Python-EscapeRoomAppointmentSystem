from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time_slot', 'num_participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time_slot': forms.Select(choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening')]),
            'num_participants': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }