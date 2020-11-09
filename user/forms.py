from django import forms


class AddMavpForm(forms.Form):
    facility_short = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Facility Identifier'
    }))
    facility_long = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Facility Name'
    }))
