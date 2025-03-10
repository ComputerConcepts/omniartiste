from django import forms
from .models import Applicant

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['name', 'email', 'phonenumber', 'resume', 'portfolio', 'coverletter']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': True}),
            'phonenumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'required': True}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Portfolio Link'}),
            'coverletter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Cover Letter'}),
        }
