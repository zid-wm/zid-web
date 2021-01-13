from django import forms


class NewEventForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    banner = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'form-control'}))
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
        label='Event Start (YYYY-MM-DD HH:MMz)'
    )
    end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
        label='Event End (YYYY-MM-DD HH:MMz)'
    )
    host = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))


class EditEventForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    banner = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'form-control'}), required=False)
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    host = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))


class AddPositionForm(forms.Form):
    callsign = forms.CharField(
        max_length=16, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Callsign'
        }))
