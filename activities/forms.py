from django import forms
from .models import EventParticipant

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventParticipant
        fields = ['email', 'full_name', 'telephone']   # add more fields if needed
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event

        # Make email required
        self.fields['email'].required = True

        # Add form-control class to all fields if not already present
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
            elif 'form-control' not in field.widget.attrs['class']:
                field.widget.attrs['class'] += ' form-control'

        if self.event and self.event.is_free:
            self.fields['full_name'].help_text = "Optional for free events"

    def clean_email(self):
        email = self.cleaned_data['email']
        if EventParticipant.objects.filter(event=self.event, email=email).exists():
            raise forms.ValidationError("This email is already registered for this event.")
        return email
