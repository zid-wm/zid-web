from django import forms


class RoutesForm(forms.Form):
    dep_apt = forms.CharField(label='Departure Airport', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Departure Airport'}))
    arr_apt = forms.CharField(label='Arrival Airport', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Arrival Airport'}))

class StaffingForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={'class':'form-control'}))
    organization = forms.CharField(label='Organization', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label='Event Description (including requested staffing)', widget=forms.TextInput(attrs={'class':'form-control'}))