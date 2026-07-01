from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('first_name', 'last_name', 'phone_number', 'subject', 'description')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name',
                'class': 'form-input',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name',
                'class': 'form-input',
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '+91 98765 43210',
                'class': 'form-input',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'e.g. Custom wardrobe quote',
                'class': 'form-input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project...',
                'class': 'form-textarea',
                'rows': 5,
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'subject': 'Subject',
            'description': 'Description',
        }