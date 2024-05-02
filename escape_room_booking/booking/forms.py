import re
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'start_time', 'end_time', 'num_participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            'end_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            'num_participants': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
    
    def validate_time(self, time):
        time_str = time.strftime('%H:%M')
        pattern = r'^([01]\d|2[0-3]):([0-5]\d)$'
        if not re.match(pattern, time_str):
            raise forms.ValidationError('Enter a valid time.')
        return time

    
    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        print(f"Cleaned start_time: {start_time}")
        print(f"Type of start_time: {type(start_time)}")
        if not self.validate_time(start_time):
            raise forms.ValidationError("Invalid start time format. Please use HH:MM AM/PM format.")
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        print(f"Cleaned end_time: {end_time}")
        print(f"Type of end_time: {type(end_time)}")
        if not self.validate_time(end_time):
            raise forms.ValidationError("Invalid end time format. Please use HH:MM AM/PM format.")
        return end_time
